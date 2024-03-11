import discord

from discord import Intents
from discord.ext import commands

TOKEN = "TOKEN_DO_BOT_DISCORD"

intents = Intents.default()
intents.messages = True
description = "Um bot teste"

bot = commands.Bot(command_prefix="!", intents=intents, description=description)

@bot.event
async def on_ready():
    print(f"Tô dentro! Eu me chamo {bot.user.name}")

    # Faz uma saudação sempre que é iniciado
    # Manda para todos os canais de texto
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                with open('src/saudacao.gif', 'rb') as f:
                    picture = discord.File(f)
                    await channel.send("Olá! Estou online e pronto para interagir.", file=picture)

@bot.event
async def on_message(message):
    print(f"Menssagem Recebida: {message.content} ") # Apenas para depuração, fora disso é anti ético

    if message.author == bot.user:
        return
    await bot.process_commands(message)

@bot.command(name='oi', help='Tente dizer oi "!oi')
async def oi(ctx):
    await ctx.send("Olá! Como vai meu mestre!")

bot.run(TOKEN)