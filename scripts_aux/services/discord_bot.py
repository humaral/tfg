import discord, os, json, logging, pyogg, opuslib, threading, queue, time, io, uuid, re, asyncio
from discord.ext import commands, voice_recv
from dotenv import load_dotenv
import numpy as np
from vosk import Model, KaldiRecognizer, SetLogLevel
from scipy.signal import resample_poly
from normalizar import transcribir_numeros_letras
from dialogflow import enviar_texto
from google.cloud import speech

#TODO colgar llamada y callarse al identificar que habla

for name in logging.root.manager.loggerDict: #Silencia los logs de discord
    logging.getLogger(name).setLevel(logging.CRITICAL)
SetLogLevel(-1) #Silencia los logs de Vosk

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

SILENCE_THRESHOLD = 1.2
USE_LOCAL_STT = False
END_CALL = threading.Event()

if USE_LOCAL_STT:
    print("Cargando modelo Vosk...")
    try:
        model = Model(os.getenv("VOSK_MODEL_PATH"))
        print("\nModelo cargado en local.")
    except:
        print("\nNo se ha podido cargar el modelo.")
        exit()


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("DIALOGFLOW_CREDENTIALS")


intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


class OpusDecoder:
    def __init__(self, rate=48000, channels=1):
        self.decoder = opuslib.Decoder(rate, channels)
    
    def decode(self, opus_bytes):
        if not opus_bytes:
            return None
        try:
            pcm48 = self.decoder.decode(opus_bytes, frame_size=960, decode_fec=True)
            pcm48 = np.frombuffer(pcm48, dtype=np.int16).astype(np.float32)
            return resample_poly(pcm48, up=1, down=3).astype(np.int16).tobytes()
        except opuslib.exceptions.OpusError:
            return None


class STTWorkerVosk(threading.Thread):
    def __init__(self, audio_input_queue, text_queue):
        super().__init__(daemon=True)
        self.audio_input_queue = audio_input_queue
        self.text_queue = text_queue
        self.recognizer = KaldiRecognizer(model, 16000)
        self.last_audio_time = time.time()

    def final_frase(self):
        res = json.loads(self.recognizer.FinalResult())
        txt = res.get("text", "").strip()
        if txt:
            txt = transcribir_numeros_letras(txt)
            print(f"[USER]: {txt}")
            self.text_queue.put(txt)
        
    def run(self):
        while True:
            try:
                pcm16k = self.audio_input_queue.get(timeout=0.1)
            except queue.Empty:
                if time.time() - self.last_audio_time > SILENCE_THRESHOLD:
                    self.final_frase()
                    self.last_audio_time = time.time()
                continue

            if pcm16k is None:
                self.text_queue.put(None)
                break
            
            self.last_audio_time = time.time()
            self.recognizer.AcceptWaveform(pcm16k)

class STTWorkerGoogle(threading.Thread):
    def __init__(self, audio_input_queue, text_queue):
        super().__init__(daemon=True)
        self.audio_input_queue = audio_input_queue
        self.text_queue = text_queue
        self.client = speech.SpeechClient()
        self.config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="es-ES",
            enable_automatic_punctuation=False
        )

        self.last_audio_time = time.time()
        self.buffer = bytearray()

    def final_frase(self):
        if not self.buffer:
            return
        audio_bytes = bytes(self.buffer)
        self.buffer = bytearray()
        try:
            audio = speech.RecognitionAudio(content=audio_bytes)
            response = self.client.recognize(config=self.config, audio=audio)
            for result in response.results:
                txt = result.alternatives[0].transcript.strip()
                if txt:
                    txt = transcribir_numeros_letras(txt)
                    print(f"[USER]: {txt}")
                    self.text_queue.put(txt)
        except Exception as e:
            print(f"Error en Google STT: {e}")
    
    def run(self):
        while True:
            try:
                pcm16k = self.audio_input_queue.get(timeout=0.1)
                
            except queue.Empty:
                if self.buffer and (time.time() - self.last_audio_time > SILENCE_THRESHOLD):
                    self.final_frase()
                    self.last_audio_time = time.time()
                continue
            
            if pcm16k is None:
                self.text_queue.put(None)
                break

            self.last_audio_time = time.time()
            self.buffer.extend(pcm16k)
            

class AgentWorker(threading.Thread):
    def __init__(self, text_queue, audio_output_queue, session_id, vc, member, bot):
        super().__init__(daemon=True)
        self.text_queue = text_queue
        self.audio_output_queue = audio_output_queue
        self.session_id = session_id
        self.welcome_done = False

        self.vc = vc
        self.member = member
        self.bot = bot

    def conexion_dialogflow(self, texto=None, bienvenida=False):
        texto_respuesta, audio_respuesta, accion_respuesta = enviar_texto(self.session_id, user_text=texto, bienvenida=bienvenida)
        txt = re.sub(r'<[^>]+>', '', texto_respuesta)
        print(f"[BOT]: {txt}")
        self.audio_output_queue.put(audio_respuesta)
        

        if accion_respuesta in ["cancelar", "tramite_certificado_empadronamiento.crear_peticion", "tramite_cita_AEAT.crear_peticion", "tramite_tarjeta_SACYL.crear_peticion"]:
            print(f"Acción '{accion_respuesta}' detectada. Finalizando llamada.")
            self.audio_output_queue.put(None) 
            asyncio.run_coroutine_threadsafe(finalizar_llamada(self.vc, self.member), self.bot.loop)


    def run(self):
        if not self.welcome_done:
            self.conexion_dialogflow(bienvenida=True)
            self.welcome_done = True

        while True:
            user_text = self.text_queue.get()
            if user_text is None:
                self.audio_output_queue.put(None)
                break

            self.conexion_dialogflow(texto=user_text)
            
class TTSWorker(threading.Thread):
    def __init__(self, audio_output_queue, vc):
        super().__init__(daemon=True)
        self.vc = vc
        self.audio_output_queue = audio_output_queue

    def run(self):
        while True:
            audio16k = self.audio_output_queue.get()

            if audio16k is None:
                self.audio_output_queue.task_done()
                break

            try:

                pcm16 = np.frombuffer(audio16k, dtype=np.int16).astype(np.float32)
                pcm48 = resample_poly(pcm16, up=3, down=1)

                pcm48 = np.repeat(pcm48[:, None], 2, axis=1).flatten()
                
                pcm48 = np.clip(pcm48, -32768, 32767).astype(np.int16).tobytes()
                
                source = discord.PCMAudio(io.BytesIO(pcm48))

                self.vc.play(source)

                while self.vc.is_playing(): 
                    time.sleep(0.01)

            except Exception as e:
                print("Error reproduciendo TTS:", e)
            
            self.audio_output_queue.task_done()


class VoskSink(voice_recv.AudioSink):
    def __init__(self, audio_input_queue):
        super().__init__()
        self.decoder = OpusDecoder()
        self.audio_input_queue = audio_input_queue

    def wants_opus(self):
        return True
    
    def write(self, user, data):
        if data.opus is None:
            return

        pcm_16k = self.decoder.decode(data.opus)
        if pcm_16k is None:
            return
        try:
            self.audio_input_queue.put_nowait(pcm_16k)
        except queue.Full:
            print("[WARNNING] La cola de audio está llena, se perdió un paquete.")
            pass

    def cleanup(self):
        pass


@bot.event
async def on_ready():
    print(f'\nEl bot {bot.user} se ha conectado correctamente a Discord')


@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None and before.channel != after.channel:
        if not member.bot and member.voice is not None:
            canal = after.channel
            print(f"\n{member} se ha conectado a {canal}.")

            users = [user for user in canal.members if not user.bot]
            if len(users)==1:
                if canal.guild.voice_client is None:

                    voz = await canal.connect(cls=voice_recv.VoiceRecvClient)
                    print(f"\n{bot.user} se ha conectado a {canal}.")

                    audio_input_queue = queue.Queue(maxsize=50)
                    text_queue = queue.Queue()
                    audio_output_queue = queue.Queue()
                    session_id = f"discord-{member.id}-{uuid.uuid4()}"

                    if USE_LOCAL_STT:
                        transcriptor = STTWorkerVosk(audio_input_queue, text_queue)
                    else:
                        transcriptor = STTWorkerGoogle(audio_input_queue, text_queue)
                    logica = AgentWorker(text_queue, audio_output_queue, session_id, voz, member, bot)
                    reproductor = TTSWorker(audio_output_queue, voz)

                    transcriptor.start()
                    logica.start()
                    reproductor.start()

                    voz.audio_input_queue = audio_input_queue
                    voz.audio_output_queue = audio_output_queue
                    voz.listen(VoskSink(audio_input_queue))
            else:
                await member.move_to(None)
                print(f'{canal} ocupado. Expulsando a {member}.')


    if before.channel is not None:
        canal = before.channel
        print(f"\n{member} ha salido de {canal}.")
        voz = canal.guild.voice_client
        if voz is None:
            return
        users = [user for user in canal.members if not user.bot]
        if len(users)==0:
            try:
                voz.audio_input_queue.put(None)
            except:
                pass
            await voz.disconnect(force=True)

async def finalizar_llamada(voz, member=None):

    if voz is None or not voz.is_connected():
        return
    
    voz.audio_output_queue.join()
    try:
        voz.audio_input_queue.put(None)
    except:
        pass

    if member is not None and member.voice:
        try:
            await member.move_to(None)
        except:
            pass

    await voz.disconnect(force=True)

bot.run(DISCORD_TOKEN)