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
