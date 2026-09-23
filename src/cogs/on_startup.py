# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Module for handling bot startup events and slash command synchronization."""

import asyncio

import discord
from discord.ext import commands


class SyncCog(commands.Cog):
    """Cog specifically for sync and login events."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the SyncCog."""
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Change the bot's status to Do Not Disturb."""
        try:
            await self.bot.tree.sync()
            await asyncio.sleep(0.5)
            await self.bot.change_presence(activity=None, status=discord.Status.dnd)
        except discord.Forbidden, discord.HTTPException:
            pass


async def setup(bot: commands.Bot) -> None:
    """Add SyncCog to the bot."""
    await bot.add_cog(SyncCog(bot))
