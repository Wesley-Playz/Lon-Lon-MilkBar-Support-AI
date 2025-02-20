import discord
from discord.ext import commands
import requests
import json

# Load the token from secrets.json
def load_token():
    with open("secrets.json", "r") as file:
        secrets = json.load(file)
    return secrets["discord_token"]

# Your Flask API URL
API_URL = "http://localhost:1423/support"

# Create bot with necessary intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
bot = commands.Bot(command_prefix='/', intents=intents)

# Register bot commands
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    print(f"Logged in as {bot.user}")

# Define the /support command as a slash command
@bot.tree.command(name="support", description="Get help with an issue related to the mod.")
async def support(interaction: discord.Interaction, issue: str):
    # Send a message that the bot is "thinking..."
    await interaction.response.send_message("The Lon Lon MilkBar Support Bot is thinking...", ephemeral=False)
    
    # Prepare the data to send to your Flask API
    payload = {"query": issue}
    headers = {"Content-Type": "application/json"}

    # Send a POST request to your Flask API
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            # Extract the AI response from the API
            ai_response = response.json().get("response", "Sorry, no response received.")

            # Edit the original message with the AI response
            await interaction.edit_original_response(content=f"**Support Response:**\n{ai_response}")
        else:
            await interaction.edit_original_response(content="Sorry, there was an issue fetching the response from the AI.")
    except Exception as e:
        await interaction.edit_original_response(content=f"Error: {str(e)}")

# Run the bot
bot.run(load_token())

