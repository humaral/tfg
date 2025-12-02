import discord, os, asyncio, threading, time
from discord.ext import commands, voice_recv
from dotenv import load_dotenv
import numpy as np
import logging
import pyogg, opuslib, librosa
from vosk import Model, KaldiRecognizer

logging.getLogger('discord').setLevel(logging.WARNING)
logging.getLogger('discord.gateway').setLevel(logging.ERROR)
logging.getLogger('discord.voice_state').setLevel(logging.ERROR)
logging.getLogger('discord.ext.voice_recv').setLevel(logging.ERROR)
logging.getLogger('discord.ext.voice_recv.reader').setLevel(logging.ERROR)
logging.getLogger('discord.ext.voice_recv.opus').setLevel(logging.ERROR)

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

model = Model(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)), "script\\vosk-model-small-es-0.42")))

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

class OpusDecoder:
    def __init__(self, rate=48000, channels=1):
        self.rate = rate
        self.channels = channels
        self.decoder = opuslib.Decoder(self.rate, self.channels)
    
    def decode(self, opus_bytes):
        pcm = self.decoder.decode(opus_bytes, frame_size=960, decode_fec=False)
        pcm_array = np.frombuffer(pcm, dtype=np.int16)
        return pcm_array


class WhispersSink(voice_recv.AudioSink):
    def __init__(self):
        super().__init__()
        self.buffer = bytearray()
        self.lock = threading.Lock()
        self.decoder = OpusDecoder(rate=48000, channels=1)
        threading.Thread(target=self.transcription_loop, daemon=True).start()
    
    def wants_opus(self):
        return True
    
    def write(self, user, data):
        if data.opus is None:
            return
        
        try:
            pcm_array = self.decoder.decode(data.opus)
        except Exception as e:
            return

        with self.lock:
            self.buffer.extend(pcm_array.tobytes())
            
    def transcription_loop(self):
        while True:
            time.sleep(0.8)

            with self.lock:
                size = len(self.buffer)

            if size < 48000 * 2 * 2.0:
                continue
            
            with self.lock:
                pcm_bytes = bytes(self.buffer)
                self.buffer = bytearray()
                
            
            self.transcribe(pcm_bytes)

    def transcribe(self, pcm_bytes):
        pcm_array = np.frombuffer(pcm_bytes, dtype=np.int16)
        audio_float = pcm_array.astype(np.float32) / 32768.0
        audio_resampled = librosa.resample(audio_float, orig_sr=48000, target_sr=16000)
        result = model.transcribe(audio_float, language="es", beam_size=5)
        text = result.get("text", "").strip()
        if text:
            asyncio.run_coroutine_threadsafe(
                self.send_transcription(text),
                bot.loop
            )

    async def send_transcription(self, text):
        print(f"TRANSCRIPCION: {text}")

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
                vc = await channel.connect(
                    cls=voice_recv.VoiceRecvClient,
                    self_mute=False,
                    self_deaf=False
                )
                vc.listen(WhispersSink())
    if before.channel is not None:
        channel = before.channel
        vc = channel.guild.voice_client
        if vc is None or vc.channel !=channel:
            return
        humans = [m for m in channel.members if not m.bot]
        if len(humans)==0:
            await vc.disconnect(force=True)


bot.run(DISCORD_TOKEN)