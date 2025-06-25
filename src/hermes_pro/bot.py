# bot.py - The new Discord version

import os
import discord
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

# FastAPI backend URL
API_ENDPOINT = "http://127.0.0.1:8000/query"

# --- Discord Bot Setup ---
# Intents are like permissions. We need to specify what our bot needs to do.
intents = discord.Intents.default()
intents.message_content = True # This is required to read message content

# Create a client instance
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """
    This function runs when the bot successfully connects to Discord.
    """
    print(f'--> Hermes Bot is now online as {client.user}')

@client.event
async def on_message(message):
    """
    This function runs on every message in every channel the bot can see.
    """
    # Rule 1: Don't let the bot reply to itself, to avoid infinite loops.
    if message.author == client.user:
        return

    # Rule 2: Only reply if the bot is mentioned.
    if client.user.mentioned_in(message):
        # Extract the actual question by removing the bot mention
        # e.g., "@Hermes-Assistant what is FastAPI?" -> "what is FastAPI?"
        user_question = message.content.split('>', 1)[-1].strip()
        print(f"Received question from {message.author}: {user_question}")

        # Show the user that the bot is "thinking"
        async with message.channel.typing():
            # Call the backend API
            try:
                response = requests.post(API_ENDPOINT, json={"query": user_question})

                if response.status_code == 200:
                    api_response = response.json()
                    answer = api_response.get("answer", "Sorry, I got a response but no answer.")
                else:
                    answer = f"My API brain responded with an error: {response.status_code}"

            except requests.exceptions.RequestException as e:
                print(f"Error calling API: {e}")
                answer = "Sorry, I can't reach my brain right now. The API server might be down."

        # Send the final answer as a reply to the user's message
        await message.reply(answer)


# --- Start the Bot ---
if __name__ == "__main__":
    if not DISCORD_BOT_TOKEN:
        print("Error: DISCORD_BOT_TOKEN not found. Please check your .env file.")
    else:
        print("--> Starting Hermes Bot for Discord...")
        client.run(DISCORD_BOT_TOKEN)