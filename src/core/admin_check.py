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

"""Module providing decorators for administrative permission checks."""

import asyncio
import contextlib

import discord
from discord import app_commands
from discord.ext import commands

from core.config import ADMINS


def admin_check() -> commands.check:
    """Checks does the author of the context (ctx) have admin permissions.

    Works with prefix and hybrid commands. Does not work with slash only commands.

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
            if ctx.message:
                with contextlib.suppress(discord.Forbidden, discord.HTTPException):
                    await ctx.message.delete()
            with contextlib.suppress(discord.Forbidden, discord.HTTPException):
                await message.delete()
        else:
            await ctx.interaction.response.send_message(msg, ephemeral=True)

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
            "You don't have required permissions to do that.",
            ephemeral=True,
        )
        return False

    return app_commands.check(predicate)
