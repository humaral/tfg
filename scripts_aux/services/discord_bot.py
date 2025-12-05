import discord, os, asyncio, json, logging, pyogg, opuslib, threading, queue, time
from discord.ext import commands, voice_recv
from dotenv import load_dotenv
import numpy as np
from vosk import Model, KaldiRecognizer, SetLogLevel
from scipy.signal import resample_poly


for name in logging.root.manager.loggerDict: #Silencia los logs de discord
    logging.getLogger(name).setLevel(logging.CRITICAL)
SetLogLevel(-1) #Silencia los logs de Vosk

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

print("Cargando modelo Vosk...")
try:
    model = Model(os.getenv("VOSK_MODEL_PATH"))
    print("\nModelo cargado en local.")
except:
    print("\nNo se ha podido cargar el modelo.")
    exit()

SILENCE_THRESHOLD = 1.5

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
        pcm = self.decoder.decode(opus_bytes, frame_size=960, decode_fec=False)
        return np.frombuffer(pcm, dtype=np.int16)

class VoskWorker(threading.Thread):
    def __init__(self, audio_queue):
        super().__init__(daemon=True)
        self.audio_queue = audio_queue
        self.recognizer = KaldiRecognizer(model, 16000)
        self.last_audio_time = time.time()

    def forzar_final(self):
        res = json.loads(self.recognizer.FinalResult())
        txt = res.get("text", "").strip()
        if txt:
            print(f"\nUser: {txt}")
        return txt
        
    def run(self):
        while True:
            try:
                pcm16k = self.audio_queue.get(timeout=0.1)
            except queue.Empty:
                if time.time() - self.last_audio_time > SILENCE_THRESHOLD:
                    self.forzar_final()
                    self.last_audio_time = time.time()
                continue

            if pcm16k is None:
                break
            
            self.last_audio_time = time.time()
            self.recognizer.AcceptWaveform(pcm16k)


class VoskSink(voice_recv.AudioSink):
    def __init__(self, audio_queue):
        super().__init__()
        self.decoder = OpusDecoder()
        self.audio_queue = audio_queue

    def wants_opus(self):
        return True
    
    def write(self, user, data):
        if data.opus is None:
            return
        
        pcm48k = self.decoder.decode(data.opus).astype(np.float32)
        
        pcm_16k = resample_poly(pcm48k, up=1, down=3).astype(np.int16).tobytes()
        
        try:
            self.audio_queue.put_nowait(pcm_16k)
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

                    audio_queue = queue.Queue(maxsize=50)
                    transcriptor = VoskWorker(audio_queue)
                    transcriptor.start()

                    voz = await canal.connect(cls=voice_recv.VoiceRecvClient)
                    print(f"\n{bot.user} se ha conectado a {canal}.")
                    voz.audio_queue = audio_queue
                    voz.transcriptor = transcriptor
                    voz.listen(VoskSink(audio_queue))
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
                voz.audio_queue.put_nowait(None)
            except:
                pass

            await voz.disconnect(force=True)


bot.run(DISCORD_TOKEN)