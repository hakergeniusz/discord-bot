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

"""Module for global error handling for both prefix and slash commands."""

import asyncio
import traceback

import discord
from discord import app_commands
from discord.ext import commands


class ErrorHandler(commands.Cog):
    """Cog for handling errors globally in the bot."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the ErrorHandler cog."""
        self.bot = bot

    async def cog_load(self) -> None:
        """Set up the app command error handler on cog load."""
        self.bot.tree.on_error = self.on_app_command_error

    async def on_app_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ) -> None:
        """Handle errors in slash commands."""
        if isinstance(error, app_commands.CheckFailure):
            if isinstance(error, app_commands.CommandOnCooldown):
                await interaction.response.send_message(
                    f"You are on cooldown. Please try again in {error.retry_after:.2f}"
                    " seconds.",
                    ephemeral=True,
                )
            return
        if isinstance(error, app_commands.CommandInvokeError):
            error = error.original

        print(f"App Command Error: {error}")
        traceback.print_exception(type(error), error, error.__traceback__)

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        """Handle errors in prefix and hybrid commands."""
        if isinstance(error, commands.CheckFailure):
            return

        if isinstance(error, commands.CommandInvokeError):
            error = error.original

        print(f"Command Error: {error}")
        traceback.print_exception(type(error), error, error.__traceback__)
        if isinstance(error, commands.CommandOnCooldown):
            if ctx.interaction:
                await ctx.interaction.response.send_message(
                    f"You are on cooldown. Please try again in {error.retry_after:.2f}"
                    " seconds.",
                    ephemeral=True,
                )
                return
            creply = await ctx.send(
                f"You are on cooldown. Please try again in {error.retry_after:.2f}"
                " seconds."
            )
            await asyncio.sleep(3)
            try:
                await ctx.message.delete()
            except discord.Forbidden, discord.HTTPException:
                pass
            try:
                await creply.delete()
            except discord.Forbidden, discord.HTTPException:
                pass
            return


async def setup(bot: commands.Bot) -> None:
    """Add ErrorHandler cog to the bot."""
    await bot.add_cog(ErrorHandler(bot))
