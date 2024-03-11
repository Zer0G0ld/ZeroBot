import discord
import asyncio
import random

from discord import Intents
from discord.ext import commands

TOKEN = "TOKEN_DISCORD"

intents = Intents.default()
intents.messages = True
description = "Um bot teste"

bot = commands.Bot(command_prefix="$", intents=intents, description=description)

# Rastreadores
sorteios_em_andamento = {} # Dicionário para rastrear os sorteios em andamento
votacoes_em_andamento = {} # Dicionário para rastrear as votações em andamento

@bot.event
async def on_ready():
    print(f"=================================")
    print(f"Estou Online como {bot.user.name}")
    print(f"=================================")

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

@bot.command(name='oi', help='Tente dizer oi')
async def oi(ctx):
    respostas = ["Olá!", "Oi, tudo bem?", "E ai? como vai?", "Oi!", "Olá! como vai meu mestre?", "Olá mestre!", "Bem-vindo de volta mestre"]
    await ctx.send(random.choice(respostas))

@bot.command(name='cls', help='Limpa mensagens do chat')
async def clear(ctx, *, argumento=None):
    if argumento is None:
        await ctx.channel.purge(limit=1000)  # Se nenhum argumento é fornecido, limpa 1000 mensagens
        print(f"Mensagens apagadas, as ultimas 1000 mensagens")
    elif argumento == '-a':
        for channel in ctx.guild.text_channels:
            await channel.purge(limit=1000)  # Limpa 1000 mensagens em cada canal de texto
    else:
        if argumento.startswith('<@') and argumento.endswith('>'):  # Verifica se o argumento é uma menção de usuário
            user_id = int(argumento[2:-1])
            member = ctx.guild.get_member(user_id)
            if member:
                check = lambda m: m.author == member
                await ctx.channel.purge(limit=1000, check=check)  # Limpa 1000 mensagens apenas do usuário mencionado
        else:
            await ctx.send("Formato inválido! Use `$cls` para limpar todo o chat, `$cls -a` para limpar todos os canais de texto ou `$cls @nome_do_usuario` para limpar as mensagens do usuário mencionado.")

@bot.command
async def trivia(ctx):
    await ctx.send("Bem vindo ao game Trivia! Qual a capital de Israel? ")
    def check(m):
        return m.author == ctx.author
    try:
        answer = await bot.wait_for('message', timeout=10.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("Tempo esgotado chefe!")
        return
    if answer.content.lower() == "Jerusalém":
        await ctx.send("Correto!")
    else:
        await ctx.send("Incorreto! A resposta correta é Jerusalém.")

@bot.command(name='votacao', help='Inicia uma votação com as escolhas fornecidas e o tempo especificado')
async def votacao(ctx, tempo_minutos: int = 1, *choices: str):
    if ctx.author.id in votacoes_em_andamento:
        await ctx.send("Você já tem uma votação em andamento!")
        return
    
    if len(choices) < 2:
        await ctx.send("Você precisa fornecer pelo menos duas opções para a votação.")
        return
    
    await ctx.send(f"Votação iniciada! Este votação encerrará em {tempo_minutos} minutos.")
    votacoes_em_andamento[ctx.author.id] = True
    
    # Formata as opções de votação
    formatted_choices = "\n".join([f"{index + 1}. {choice}" for index, choice in enumerate(choices)])
    message = await ctx.send(f"Escolha uma opção digitando o número correspondente:\n{formatted_choices}")
    
    # Adiciona as reações para cada opção de votação
    for i in range(1, len(choices) + 1):
        await message.add_reaction(f"{i}\u20e3")  # Adiciona reação com emoji numérico

    await asyncio.sleep(tempo_minutos * 60)  # Aguarda o tempo especificado em minutos

    del votacoes_em_andamento[ctx.author.id]
    await ctx.send("O votação encerrou!")

@bot.command(name='sorteio', help='Inicia um sorteio com o tempo especificado')
async def sorteio(ctx, tempo_minutos: int = 1):
    if ctx.author.id in sorteios_em_andamento:
        await ctx.send("Você já tem um sorteio em andamento!")
        return
    
    await ctx.send(f"Sorteio iniciado! Este sorteio encerrará em {tempo_minutos} minutos. Reaja com 🎉 para participar!")
    sorteios_em_andamento[ctx.author.id] = True
    
    message = await ctx.send("O sorteio começou!")
    await message.add_reaction('🎉')

    def check(reaction, user):
        return str(reaction.emoji) == '🎉' and user != bot.user

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=tempo_minutos * 60.0, check=check)
    except asyncio.TimeoutError:
        del sorteios_em_andamento[ctx.author.id]
        await ctx.send("Ninguém participou do sorteio. Sorteio cancelado.")
    else:
        del sorteios_em_andamento[ctx.author.id]
        winner = user
        await ctx.send(f"Parabéns, {winner.mention}! Você ganhou o sorteio!")

bot.run(TOKEN)
