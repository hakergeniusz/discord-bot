# Copyright (C) 2026 hakergeniusz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import discord
from discord.ext import commands
from core.config import TOKEN

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.load_cogs()

    async def load_cogs(self):
        cogs_path = os.path.join(os.path.dirname(__file__), "cogs")
        count = 0
        for root, _, files in os.walk(cogs_path):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    relative_path = os.path.relpath(os.path.join(root, file), os.path.dirname(__file__))
                    module_path = relative_path.replace(os.sep, ".")[:-3]
                    try:
                        await self.load_extension(module_path)
                        print(f"Successfully loaded: {module_path}")
                        count += 1
                    except Exception as e:
                        print(f"Failed to load {module_path}: {e}")

        if count == 0:
            print('Could not load any cogs. ')
            exit()
        print(f"--- Finished loading {count} cogs ---")

bot = MyBot()

if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except KeyboardInterrupt:
        print("\nShutting down the bot...")
