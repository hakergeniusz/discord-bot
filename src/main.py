# Copyright (c) 2025-2026 hakergeniusz
#
# Licensed under the EUPL, Version 1.2 or - as soon they will be approved by the European
# Commission - subsequent versions of the EUPL (the "Licence"); You may not use this work
# except in compliance with the Licence.
#
# You may obtain a copy of the Licence at:
# https://joinup.ec.europa.eu/software/page/eupl
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the Licence for the specific language
# governing permissions and limitations under the Licence.

"""Main entry point for the Discord bot. Handles bot initialization and cog loading."""

import asyncio
import contextlib
import sys
from pathlib import Path

import discord
from discord.ext import commands

from core.config import PREFIX, TOKEN
from core.logger import get_logger

logger = get_logger(__name__)

# Use ProactorEventLoop on Windows for better compatibility with subprocesses/FFmpeg
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


class MyBot(commands.Bot):
    """Custom Bot class with extension loading capabilities."""

    def __init__(self) -> None:
        """Initialize the bot with default intents and command prefix."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        super().__init__(command_prefix=PREFIX, intents=intents)

    async def setup_hook(self) -> None:
        """Set up the bot after login, loading all extensions."""
        await self.load_cogs()

    async def load_cogs(self) -> None:
        """Walk through the cogs directory and load all Python files as extensions.

        Raises:
            RuntimeError: If no cogs could be loaded.
        """
        cogs_path: Path = Path(__file__).resolve().parent / "cogs"  # noqa: ASYNC240
        count: int = 0
        for path in cogs_path.rglob("*.py"):  # noqa: ASYNC240
            if path.name == "__init__.py":
                continue

            relative_path = path.relative_to(cogs_path.parent)
            module_path = ".".join(relative_path.with_suffix("").parts)
            try:
                await self.load_extension(module_path)
                count += 1
            except Exception:
                logger.exception("Failed to load %s", module_path)

        if count == 0:
            msg = "Could not load any cogs."
            logger.error(msg)
            raise RuntimeError(msg)
        logger.info("--- Finished loading %d cogs ---", count)


bot = MyBot()


def main() -> None:
    """Entry point for the bot."""
    with contextlib.suppress(KeyboardInterrupt):
        bot.run(TOKEN)


if __name__ == "__main__":
    main()
