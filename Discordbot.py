import os
import discord
import openai
from discord.ext import commands

# Set OpenAI API key
openai.api_key = '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'

# Set up the bot with the command prefix '!'
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)

# Function to generate a response from ChatGPT
async def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=50,
            n=1,
            temperature=0.7,
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error: {e}")
        return None

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name='!chat for help'))

@bot.command(name='hello', help='Say hello to the bot.')
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')

# Command to interact with ChatGPT
@bot.command(name='chat', help='Chat with GPT-3.')
async def chat(ctx, *, prompt):
    response = await generate_response(prompt)
    await ctx.send(response)

# Replace 'your_bot_token_here' with your bot's token
bot.run('MTA4NTQ2MDY2ODY3ODk0Mjc2MQ.GBlV4m.m7PHq0HCXMcCrdbyBSvlsiOmJgAh54Ycs5Uts8')
