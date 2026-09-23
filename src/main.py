# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

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
        cogs_path: Path = Path(__file__).resolve().parent / "cogs"  # ruff: ignore[blocking-path-method-in-async-function]
        count: int = 0
        for path in cogs_path.rglob("*.py"):  # ruff: ignore[blocking-path-method-in-async-function]
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
