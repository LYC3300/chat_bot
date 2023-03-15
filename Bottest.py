import discord
from discord.ext import commands

TOKEN = 'MTA4NTQ2MDY2ODY3ODk0Mjc2MQ.GBlV4m.m7PHq0HCXMcCrdbyBSvlsiOmJgAh54Ycs5Uts8'

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True


bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f"Message from {message.author}: {message.content}")
    print(f"Message: {message}")

    # If the message is a command, process it
    await bot.process_commands(message)

bot.run(TOKEN)