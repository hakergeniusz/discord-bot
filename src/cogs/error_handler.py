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
            return
        print(f"App Command Error: {error}")

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        """Handle errors in prefix and hybrid commands."""
        if isinstance(error, commands.CheckFailure):
            return
        print(f"Command Error: {error}")


async def setup(bot: commands.Bot) -> None:
    """Add ErrorHandler cog to the bot."""
    await bot.add_cog(ErrorHandler(bot))
