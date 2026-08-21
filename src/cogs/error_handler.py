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

"""Cog for handling errors globally in the bot."""

import asyncio
import contextlib
import typing

import discord
from discord import app_commands
from discord.ext import commands

from core.logger import get_logger

# Module-level logger
logger = get_logger(__name__)


class ErrorHandler(commands.Cog):
    """Cog for handling errors globally in the bot."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the ErrorHandler cog."""
        self.bot = bot
        logger.debug("ErrorHandler cog initialized")

    async def cog_load(self) -> None:
        """Set up the app command error handler."""
        self.bot.tree.on_error = self.on_app_command_error
        logger.debug("App command error handler set")

    @typing.override
    async def on_app_command_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        """Handle errors that occur during app command execution."""
        logger.debug("Handling app command error: %s", error)
        if isinstance(error, app_commands.CheckFailure):
            if isinstance(error, app_commands.CommandOnCooldown):
                await interaction.response.send_message(
                    f"You are on cooldown. Please try again in {error.retry_after:.2f} seconds.",
                    ephemeral=True,
                )
            logger.warning("Slash command check failure: %s", error)
            return
        if isinstance(error, app_commands.CommandInvokeError):
            error = error.original

        logger.error("Slash command exception: %s", error)

    @commands.Cog.listener()
    @typing.override
    async def on_command_error(
        self,
        ctx: commands.Context,
        error: commands.CommandError,
    ) -> None:
        """Handle errors that occur during command execution."""
        logger.debug("Handling command error: %s", error)
        if isinstance(error, commands.CheckFailure):
            logger.warning("Command check failure: %s", error)
            return

        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        logger.error("Command exception: %s", error)
        if isinstance(error, commands.CommandOnCooldown):
            message = f"You are on cooldown. Please try again in {error.retry_after:.2f} seconds."
            if ctx.interaction:
                await ctx.interaction.response.send_message(
                    message,
                    ephemeral=True,
                )
                return
            creply = await ctx.send(message)
            await asyncio.sleep(3)
            with contextlib.suppress(discord.Forbidden, discord.HTTPException):
                await ctx.message.delete()
            with contextlib.suppress(discord.Forbidden, discord.HTTPException):
                await creply.delete()
            return


async def setup(bot: commands.Bot) -> None:
    """Add ErrorHandler cog to the bot."""
    await bot.add_cog(ErrorHandler(bot))
