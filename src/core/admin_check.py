# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

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

    Returns:
        commands.check: A decorator that can be used to protect bot commands.
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
