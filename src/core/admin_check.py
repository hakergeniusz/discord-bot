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

"""Module providing decorators for administrative permission checks."""

import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from core.config import ADMINS


def admin_check() -> commands.check:
    """Checks does the author of the context (ctx) have admin permissions.

    Works with prefix and hybrid commands. Does not work with slash only commands.

    Returns:
        commands.check: A decorator that can be used to protect bot commands.

    Implementation:
        Add @admin_check() at start of command's code.
    """

    async def predicate(ctx: commands.Context) -> bool:
        user = getattr(ctx, "author", getattr(ctx, "user", None))

        if user and user.id in ADMINS:
            return True

        if ADMINS == []:
            msg = "Admin commands have been disabled."
        else:
            msg = "You don't have required permissions to do that."
        if hasattr(ctx, "send"):
            message = await ctx.send(msg)
            await asyncio.sleep(3)
            try:
                await ctx.message.delete()
            except discord.Forbidden, discord.HTTPException:
                pass
            try:
                await message.delete()
            except discord.Forbidden, discord.HTTPException:
                pass
        else:
            await ctx.response.send_message(msg, ephemeral=True)

        return False

    return commands.check(predicate)


def admin_check_slash() -> commands.check:
    """Checks does the author of the interaction have admin permissions.

    Works only with slash commands.

    Returns:
        commands.check: A decorator that can be used to protect bot commands.

    Implementation:
        Add @admin_check() at start of command's code.
    """

    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.user.id in ADMINS:
            return True
        await interaction.response.send_message(
            "You don't have required permissions to do that.", ephemeral=True
        )
        return False

    return app_commands.check(predicate)
