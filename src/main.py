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

"""Main entry point for the Discord bot. Handles bot initialization and cog loading."""

from pathlib import Path

import discord
from discord.ext import commands

from core.config import TOKEN


class MyBot(commands.Bot):
    """Custom Bot class with extension loading capabilities."""

    def __init__(self) -> None:
        """Initialize the bot with default intents and command prefix."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self) -> None:
        """Set up the bot after login, loading all extensions."""
        await self.load_cogs()

    async def load_cogs(self) -> None:
        """Walk through the cogs directory and load all Python files as extensions."""
        cogs_path = Path(__file__).resolve().parent / "cogs"
        count = 0
        for path in cogs_path.rglob("*.py"):
            if path.name == "__init__.py":
                continue

            relative_path = path.relative_to(cogs_path.parent)
            module_path = ".".join(relative_path.with_suffix("").parts)
            try:
                await self.load_extension(module_path)
                print(f"Successfully loaded: {module_path}")
                count += 1
            except Exception as e:
                print(f"Failed to load {module_path}: {e}")

        if count == 0:
            print("Could not load any cogs. ")
            raise RuntimeError("Could not load any cogs.")
        print(f"--- Finished loading {count} cogs ---")


bot = MyBot()

if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except KeyboardInterrupt:
        print("\nShutting down the bot...")
