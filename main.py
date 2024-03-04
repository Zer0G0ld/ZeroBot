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