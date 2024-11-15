"""Copyright (c) Void 2024 - Translator Bot

Comment needs to be written

Author: Void

Since: v1.0.0
"""

import os

from deep_translator import GoogleTranslator
import discord
from discord.ext import commands
from discord import app_commands
import dotenv

dotenv.load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"Synced {[command.name for command in synced]} command(s).")
    except Exception as e:
        print(f"Error syncing commands: {e}")
    print("Bot is online")

@app_commands.allowed_installs(users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.context_menu(name="Translate")
@app_commands.user_install()
async def context_menu_translate(interaction: discord.Interaction, message: discord.Message):
    text = message.content.removesuffix(" ")
    if interaction.locale.value == "en-US":
        translated = GoogleTranslator(source='auto', target='en').translate(text)
    else:
        translated = GoogleTranslator(source='auto', target=interaction.locale.value).translate(text)
    await interaction.response.send_message(translated, ephemeral=True)

bot.run(DISCORD_TOKEN)