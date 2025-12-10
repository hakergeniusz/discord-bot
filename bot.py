from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import asyncio

load_dotenv()
token = os.environ.get("ping_token")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_cogs():
    await bot.load_extension("cogs.on_startup")
    print("Loading cog 'startup behaviour'...")
    await bot.load_extension("cogs.admin")
    print("Loading cog 'Admin'...")
    await bot.load_extension("cogs.meme")
    print("Loading cog 'Meme'...")
    await bot.load_extension("cogs.utility")
    print("Loading cog 'Utility'...")
    await bot.load_extension("cogs.music")
    print("Loading cog 'Music'...")
    await bot.load_extension("cogs.f1")
    print("Loading cog 'F1'...")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(token)

asyncio.run(main())
