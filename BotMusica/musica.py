import discord
import yt_dlp

from discord.ext import commands
from discord import FFmpegPCMAudio


TOKEN = "TOKEN_DO_BOT_DISCORD"

intents = discord.Intents.default()
intents.voice_states = True

description = "Bot que tenta tocar música."
bot = commands.Bot(command_prefix='$', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f"Estou pronto! Meu nome agora é {bot.user.name}")

@bot.event
async def on_message(message):
    print(f"Mensagem Recebida: {message.content}")

    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.command()
async def play(ctx, url):
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("Você precisa estar em um canal de voz para usar este comando.")
        return

    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        vc = await voice_channel.connect()
    elif ctx.voice_client.channel != voice_channel:
        await ctx.voice_client.move_to(voice_channel)
        vc = ctx.voice_client
    else:
        vc = ctx.voice_client

    try:
        ydl_opts = {'format': 'bestaudio'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
        vc.play(FFmpegPCMAudio(url2), after=lambda e: print('Música terminada'))
    except Exception as e:
        await ctx.send(f"Ocorreu um erro ao reproduzir a música: {e}")

@bot.command()
async def pause(ctx):
    if ctx.guild.id in voice_clients:
        vc = voice_clients[ctx.guild.id]
        if vc.is_playing():
            vc.pause()
            await ctx.send("Reprodução pausada.")
        else:
            await ctx.send("Não há música sendo reproduzida para pausar.")
    else:
        await ctx.send("Não estou conectado a nenhum canal de voz.")

bot.run(TOKEN)
