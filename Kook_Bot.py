import khl
import json
import openai
import requests
from collections import defaultdict
from khl import Bot, Message
MAX_HISTORY_LENGTH = 500

BOT_TOKEN = '1/MTQwMjQ=/BQquorl8OOaK9UeHFbGYqg=='
openai.api_key = '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'
ai_name = "550C"
conversation_histories = defaultdict(list)
bot = khl.Bot(token=BOT_TOKEN)

def generate_response(user_id, prompt):
    conversation_history = conversation_histories[user_id]
    if not conversation_history:
        conversation_history.append({"role": "system", "content": f"You are a helpful assistant with name {ai_name}."})
    conversation_history.append({"role": "user", "content": prompt})
    conversation_history_str = json.dumps(conversation_history)

    # Check if the conversation_history is too long
    while len(conversation_history_str) > MAX_HISTORY_LENGTH:
        # Remove the oldest message until the conversation_history fits within the token limit
        conversation_history.pop(0)
        conversation_history_str = json.dumps(conversation_history)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
        max_tokens=4000,
        n=1,
        temperature=0.7,
    )

    assistant_response = response.choices[0].message['content']
    conversation_history.append({"role": "assistant", "content": assistant_response})
    return assistant_response

def generate_response_short(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant with name 550C."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=4000,
            n=1,
            temperature=0.7,
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error: {e}")
        return None

@bot.command(name='hello')
async def world(msg: Message):
    print(f"Message from {msg.author.id}: {msg.content}")
    await msg.reply('world!')

@bot.command(name='chat', help='Ask a question and get a response from the AI assistant.')
async def ask(msg: Message, question: str):
    author_id = msg.author.id
    print(f"Message from {author_id}: {question}")
    response = generate_response(author_id, question)
    await msg.reply(response)

@bot.command(name='ask', help='Ask a question and get a response from the AI assistant.')
async def ask(msg: Message, question: str):
    author_id = msg.author.id
    print(f"Message from {author_id}: {question}")
    response = generate_response_short(question)
    await msg.reply(response)
bot.run()



# def on_message(ws, message):
#     data = json.loads(message)
#     print(data)

#     # Check if the received message is a text message from a user
#     if data["s"] == 0 and data["d"]["type"] == 1 and data["d"]["author"]["id"] != data["d"]["bot"]["id"]:
#         prompt = data["d"]["content"]
#         user_id = data["d"]["author"]["id"]
#         command = prompt[1:].split(" ")[0].lower()
#         if prompt.startswith('!'):
#             handle_command(command, ws, data, user_id, prompt)

# def handle_command(command, ws, data, user_id, prompt):
#     if command == "help":
#         response = "Here's a list of available commands:\n!help - Shows this help message \n!ask - Ask question to 550C"
#         payload = {
#             "type": 1,
#             "target_id": data["d"]["channel_id"],
#             "content": response
#         }
#         ws.send(json.dumps(payload))
#     elif command == "ask":
#         response = generate_response(user_id,prompt)
#         # Send the response back to the chat
#         payload = {
#             "type": 1,
#             "target_id": data["d"]["channel_id"],
#             "content": response
#         }
#         ws.send(json.dumps(payload))
#     # Add more commands by extending this function
