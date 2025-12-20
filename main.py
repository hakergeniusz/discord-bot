#  Copyright (C) 2025 hakergeniusz
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import discord
from discord.ext import commands
import asyncio

token = os.environ['DISCORD_BOT_TOKEN']

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_cogs():
    """Loads all extensions (cogs)."""
    await bot.load_extension("cogs.on_startup")
    print("Loading cog 'Startup behaviour'...")
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
    await bot.load_extension('cogs.other')
    print("Loading cog 'Other'...")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(token)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Shutting down the bot...')