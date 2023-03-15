import json
import discord
import openai
from discord.ext import commands
from collections import defaultdict

from Kook_Bot import MAX_HISTORY_LENGTH

# Replace 'your_bot_token_here' with your actual Discord bot token
TOKEN = 'MTA4NTQ2MDY2ODY3ODk0Mjc2MQ.GBlV4m.m7PHq0HCXMcCrdbyBSvlsiOmJgAh54Ycs5Uts8'

# Replace 'your_api_key_here' with your actual OpenAI API key
openai.api_key = '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'

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
ai_name="550C"
conversation_histories = defaultdict(list)


# Change only the no_category default string
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)
bot = commands.Bot(command_prefix='!', intents=intents, help_command=help_command)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name='!chat for help'))



async def generate_response_new(user_id, prompt):
    conversation_history = conversation_histories[user_id]
    if not conversation_history:
        conversation_history.append({"role": "system", "content": f"You are a helpful assistant with name {ai_name}."})
    conversation_history.append({"role": "user", "content": prompt})
    # Check if the conversation_history is too long
    while len(conversation_history_str) > MAX_HISTORY_LENGTH:
        # Remove the oldest message until the conversation_history fits within the token limit
        conversation_history.pop(0)
        conversation_history_str = json.dumps(conversation_history)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
        max_tokens=150,
        n=1,
        temperature=0.7,
    )

    assistant_response = response.choices[0].message['content']
    conversation_history.append({"role": "assistant", "content": assistant_response})

    return assistant_response

async def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant with name 550C."},
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


@bot.command(name='ask', help='Ask a question and get a response from the AI assistant.')
async def ask(ctx, *, question):
    response = await generate_response_new(ctx.author.id, question)
    await ctx.send(response)

@bot.command(name='hello', help='Say hello to the bot.')
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')

# Command to interact with ChatGPT
@bot.command(name='chat', help='Chat with GPT-3 with single conversation.')
async def chat(ctx, *, prompt):
    response = await generate_response(prompt)
    await ctx.send(response)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f"Message from {message.author}: {message.content}")

    # If the message is a command, process it
    await bot.process_commands(message)

bot.load_extension("general_commands")

bot.run(TOKEN)
