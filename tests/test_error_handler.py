# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the ErrorHandler cog."""

from unittest.mock import AsyncMock, MagicMock, patch

import discord
import pytest
from discord.ext import commands

from cogs.error_handler import ErrorHandler, setup


def test_error_handler_initialization() -> None:
    """Test ErrorHandler initialization."""
    bot = MagicMock(spec=commands.Bot)
    cog = ErrorHandler(bot)
    assert cog.bot == bot


@pytest.mark.asyncio
async def test_on_app_command_error_cooldown() -> None:
    """Test ErrorHandler handling of CommandOnCooldown."""
    bot = MagicMock(spec=commands.Bot)
    cog = ErrorHandler(bot)
    interaction = AsyncMock(spec=discord.Interaction)
    interaction.response = AsyncMock()
    interaction.response.send_message = AsyncMock()
    cooldown = discord.app_commands.Cooldown(1, 5.0)
    error = discord.app_commands.CommandOnCooldown(cooldown, retry_after=5.0)

    await cog.on_app_command_error(interaction, error)

    interaction.response.send_message.assert_called_once()
    args, kwargs = interaction.response.send_message.call_args
    assert "cooldown" in args[0]
    assert kwargs["ephemeral"] is True


@pytest.mark.asyncio
async def test_cog_load_registers_app_command_handler() -> None:
    """Test cog_load installing the app command error handler."""
    bot = MagicMock(spec=commands.Bot)
    cog = ErrorHandler(bot)

    await cog.cog_load()

    assert bot.tree.on_error == cog.on_app_command_error


@pytest.mark.asyncio
async def test_on_app_command_error_check_failure() -> None:
    """Test app command errors that are plain check failures."""
    cog = ErrorHandler(MagicMock(spec=commands.Bot))
    interaction = AsyncMock(spec=discord.Interaction)
    interaction.response = AsyncMock()

    await cog.on_app_command_error(interaction, discord.app_commands.CheckFailure("nope"))

    interaction.response.send_message.assert_not_awaited()


@pytest.mark.asyncio
async def test_on_app_command_error_unwraps_invoke_error() -> None:
    """Test app command invoke errors being unwrapped before logging."""
    cog = ErrorHandler(MagicMock(spec=commands.Bot))
    interaction = AsyncMock(spec=discord.Interaction)
    interaction.response = AsyncMock()
    original = ValueError("boom")
    error = discord.app_commands.CommandInvokeError(MagicMock(), original)

    await cog.on_app_command_error(interaction, error)

    interaction.response.send_message.assert_not_awaited()


@pytest.mark.asyncio
async def test_on_command_error_check_failure() -> None:
    """Test command check failures being swallowed."""
    cog = ErrorHandler(MagicMock(spec=commands.Bot))
    ctx = AsyncMock(spec=commands.Context)

    await cog.on_command_error(ctx, commands.CheckFailure("nope"))

    ctx.send.assert_not_awaited()


@pytest.mark.asyncio
async def test_on_command_error_unwraps_invoke_error() -> None:
    """Test command invoke errors being unwrapped before logging."""
    cog = ErrorHandler(MagicMock(spec=commands.Bot))
    ctx = AsyncMock(spec=commands.Context)

    await cog.on_command_error(ctx, commands.CommandInvokeError(ValueError("boom")))

    ctx.send.assert_not_awaited()


@pytest.mark.asyncio
async def test_on_command_error_cooldown_via_interaction() -> None:
    """Test cooldown errors reported through the interaction response."""
    cog = ErrorHandler(MagicMock(spec=commands.Bot))
    ctx = AsyncMock(spec=commands.Context)
    ctx.interaction = AsyncMock()
    cooldown = commands.CommandOnCooldown(
        commands.Cooldown(1, 1.0),
        3.5,
        commands.BucketType.default,
    )

    await cog.on_command_error(ctx, cooldown)

    ctx.interaction.response.send_message.assert_awaited_once()
    sent = ctx.interaction.response.send_message.call_args.args[0]
    assert "3.50 seconds" in sent


@pytest.mark.asyncio
async def test_on_command_error_cooldown_via_context() -> None:
    """Test cooldown errors reported and cleaned up in a text channel."""
    cog = ErrorHandler(MagicMock(spec=commands.Bot))
    ctx = AsyncMock(spec=commands.Context)
    ctx.interaction = None
    ctx.send.return_value = AsyncMock()
    ctx.message = AsyncMock()
    cooldown = commands.CommandOnCooldown(
        commands.Cooldown(1, 1.0),
        1.0,
        commands.BucketType.default,
    )

    with patch("cogs.error_handler.asyncio.sleep", new=AsyncMock()):
        await cog.on_command_error(ctx, cooldown)

    assert "1.00 seconds" in ctx.send.call_args.args[0]
    ctx.message.delete.assert_awaited_once()
    ctx.send.return_value.delete.assert_awaited_once()


@pytest.mark.asyncio
async def test_on_command_error_cooldown_survives_delete_failure() -> None:
    """Test cooldown cleanup tolerating a missing permission to delete."""
    cog = ErrorHandler(MagicMock(spec=commands.Bot))
    ctx = AsyncMock(spec=commands.Context)
    ctx.interaction = None
    ctx.send.return_value = AsyncMock()
    ctx.message = AsyncMock()
    ctx.message.delete.side_effect = discord.Forbidden(MagicMock(status=403), "boom")
    cooldown = commands.CommandOnCooldown(
        commands.Cooldown(1, 1.0),
        1.0,
        commands.BucketType.default,
    )

    with patch("cogs.error_handler.asyncio.sleep", new=AsyncMock()):
        await cog.on_command_error(ctx, cooldown)

    ctx.send.return_value.delete.assert_awaited_once()


@pytest.mark.asyncio
async def test_error_handler_setup_adds_cog() -> None:
    """Test that setup registers the ErrorHandler cog."""
    bot = MagicMock(spec=commands.Bot)
    bot.add_cog = AsyncMock()

    await setup(bot)

    bot.add_cog.assert_awaited_once()
    assert isinstance(bot.add_cog.call_args.args[0], ErrorHandler)
