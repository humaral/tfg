import discord, os, asyncio, json
from discord.ext import commands, voice_recv
from dotenv import load_dotenv
import numpy as np
from vosk import Model, KaldiRecognizer
import logging, pyogg, opuslib, resampy

logging.getLogger('discord').setLevel(logging.WARNING)
logging.getLogger('discord.gateway').setLevel(logging.ERROR)
logging.getLogger('discord.voice_state').setLevel(logging.ERROR)
logging.getLogger('discord.ext.voice_recv').setLevel(logging.ERROR)
logging.getLogger('discord.ext.voice_recv.reader').setLevel(logging.ERROR)
logging.getLogger('discord.ext.voice_recv.opus').setLevel(logging.ERROR)

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


class VoskSink(voice_recv.AudioSink):
    def __init__(self, sample_rate=48000, channels=1):
        super().__init__()
        self.decoder = OpusDecoder()
        self.recognizer = KaldiRecognizer(model, 16000)
        self.buffer = bytearray()
    
    def wants_opus(self):
        return True
    
    def write(self, user, data):
        if data.opus is None:
            return
        
        pcm = self.decoder.decode(data.opus)
        
        pcm_16k = resampy.resample(
            pcm.astype(np.float32),
            48000,
            16000
        ).astype(np.int16)
        
        self.buffer.extend(pcm_16k.tobytes())
        
        chunk_size = int(16000 * 2 * 0.1)  # 0.1 s * 2 bytes/sample
        
        while len(self.buffer) >= chunk_size:
            raw = self.buffer[:chunk_size]
            self.buffer = self.buffer[chunk_size:]
            
            if self.recognizer.AcceptWaveform(bytes(raw)):
                self.print_result(self.recognizer.Result())
            else:
                self.print_result(self.recognizer.PartialResult())

    def print_result(self, result_json):
        try:
            res = json.loads(result_json)
            text = res.get("text", "").strip()
            if text:
                print(f"TRANSCRIPCION: {text}")
        except Exception as e:
            print("Error al parsear resultado:", e)        
    
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
                vc.listen(VoskSink())
    if before.channel is not None:
        channel = before.channel
        vc = channel.guild.voice_client
        if vc is None or vc.channel !=channel:
            return
        humans = [m for m in channel.members if not m.bot]
        if len(humans)==0:
            await vc.disconnect(force=True)


bot.run(DISCORD_TOKEN)