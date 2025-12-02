import os, discord, whisper, asyncio, tempfile, io, wave
from pydub import AudioSegment
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')


class WaveSink(discord.sinks.Sink):
    def __init__(self):
        super().__init__(encoding='wav')
        self.audio_data = {}

    def write(self, data, user):
        user_id = user.id
        if user_id not in self.audio_data:
            self.audio_data[user_id] = io.BytesIO()
        
        self.audio_data[user_id].write(data)
    
    def cleanup(self):
        for user_data in self.audio_data.values():
            user_data.close()
        self.audio_data.clear()


# class STTReceiver(voice_recv.AudioReader):
#     def __init__(self, voice_client):
#         super().__init__(sink=None, voice_client=voice_client)

#     def on_pcm(self, user: discord.User, pcm:bytes):
#         print(f"SE RECIVE EL AUDIO de {user}")

model = whisper.load_model("base")


intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

grabando = False


@bot.event
async def on_ready():
    print(f'El bot {bot.user} se ha conectado correctamente a Discord')


@bot.event
async def on_voice_state_update(member, before, after):
    global grabando
    if member.bot:
        return
    
    if (not before.channel) and after.channel:
        canal = after.channel
        print(f'{member.name} ha entrado en {canal.name}')

        usuarios = [user for user in canal.members if not user.bot]
        if len(usuarios) == 1:
            voz = await entrar_al_canal(canal)
            if voz:
                grabando = True
                canal_transcripcion = discord.utils.get(canal.guild.text_channels, name="transcripciones")
                asyncio.create_task(capturar_audio(voz, canal_transcripcion))

        else:
            await member.move_to(None)
            print(f'Canal {canal.name} ocupado. Expulsando a {member.name}')

    if before.channel and (not after.channel):
        canal = before.channel
        print(f'{member.name} has left {canal.name}')

        usuarios = [user for user in canal.members if not user.bot]

        if len(usuarios) == 0:
            await salir_del_canal(canal)
            grabando = False

async def entrar_al_canal(canal):
    voz = canal.guild.voice_client
    if voz and voz.is_connected():
        print(f'El bot ya está en un canal de voz')
        return voz
    
    try:
        voz = await canal.connect()
        print(f'El bot se ha unido a {canal.name}')
        return voz
    except Exception as e:
        print(f'fallo al conectarse al canal: {e}')
        return None


async def salir_del_canal(canal):
    global grabando
    voz = canal.guild.voice_client

    if voz and voz.is_connected():
        await voz.disconnect()
        grabando = False
        print(f'El bot ha abandonado {canal.name}')
    else:
        pass


async def capturar_audio(voz: discord.VoiceClient, texto: discord.TextChannel):
    global grabando

    while not voz.is_connected():
        await asyncio.sleep(0.1)

    
    while grabando and voz.is_connected():
        try:
            sink = WaveSink()
            voz.listen(
                sink,
                lambda error: asyncio.run_coroutine_threadsafe(finalizar_captura(sink, texto, error), bot.loop).result()
            )
            await asyncio.sleep(5)
            voz.stop()
            await asyncio.sleep(1)

        except Exception as e:
            print(f"Error durante la captura de audio: {e}")
            grabando = False
            voz.stop()
            break


async def finalizar_captura(sink: WaveSink, texto: discord.TextChannel, error):
    if error:
        print(f"error: {error}")
        return

    print("Fin de un fragmento de audio. Procesando...")

    for user_id, audio in sink.audio_data.items():
        
        user = bot.get_user(user_id)
        user_name = user.display_name if user else f"Usuario {user_id}"

        audio.seek(0)

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio.read())
                tmp_path = tmp.name
        except Exception as e:
            continue
        try:        
            result = model.transcribe(tmp_path, language='es')
            # print(f"Transcripción de {user_id}: {result['text']}")
            await texto.send(f"**{user_name}** dijo:\n> {result['text']}")
        except Exception as e:
            await texto.send(f"Error al transcribir el audio de {user_name}: {e}")
        finally:
            os.remove(tmp_path)
    
    sink.cleanup()


bot.run(DISCORD_TOKEN)