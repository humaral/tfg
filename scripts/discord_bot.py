import discord, os, asyncio, json, logging, pyogg, opuslib, threading, queue
from discord.ext import commands, voice_recv
from dotenv import load_dotenv
import numpy as np
from vosk import Model, KaldiRecognizer 
from scipy.signal import resample_poly

for name in logging.root.manager.loggerDict:
    logging.getLogger(name).setLevel(logging.CRITICAL)


load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

model = Model(os.path.join(os.path.dirname(__file__), "vosk-model-small-es-0.42"))


intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
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
        self.last_partial = ""
    def run(self):
        while True:
            pcm16k = self.audio_queue.get()
            if pcm16k is None:
                break
            if self.recognizer.AcceptWaveform(pcm16k):
                res = json.loads(self.recognizer.Result())
                txt = res.get("text", "").strip()
                if txt:
                    print(f"\nTRANSCRIPCION FINAL: {txt}")
                self.last_partial=""
            else:
                res = json.loads(self.recognizer.PartialResult())
                txt = res.get("partial", "").strip()
                if txt and txt != self.last_partial:
                    print(f"TRANSCRIPCION: {txt}", end="\r", flush=True)
                    self.last_partial=txt


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
            pass

    def print_result(self, result_json, final=False):
        try:
            data = json.loads(result_json)
            text = ""
            
            if final:
                text = data.get("text", "").strip()
                if text:
                    print(f"\nTRANSCRIPCION FINAL: {text}\n")
                self.last_partial = ""
            else:
                text = data.get("partial", "").strip()
                if text and text != self.last_partial:
                    print(f"TRANSCRIPCION: {text}", end="\r", flush=True)
                    self.last_partial = text
        except:
            pass

    def cleanup(self):
        pass


@bot.event
async def on_ready():
    print(f'El bot {bot.user} se ha conectado correctamente a Discord')

async def should_connect(member):
    return not member.bot and member.voice is not None

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None and before.channel != after.channel:
        if await should_connect(member):
            channel = after.channel
            if channel.guild.voice_client is None:

                audio_queue = queue.Queue(maxsize=50)
                worker = VoskWorker(audio_queue)
                worker.start()

                vc = await channel.connect(
                    cls=voice_recv.VoiceRecvClient,
                    self_mute=False,
                    self_deaf=False
                )
                vc.audio_queue = audio_queue
                vc.worker = worker
                vc.listen(VoskSink(audio_queue))

    if before.channel is not None:
        channel = before.channel
        vc = channel.guild.voice_client
        if vc is None or vc.channel !=channel:
            return
        humans = [m for m in channel.members if not m.bot]
        if len(humans)==0:
            try:
                vc.audio_queue.put_nowait(None)
            except:
                pass

            await vc.disconnect(force=True)


bot.run(DISCORD_TOKEN)