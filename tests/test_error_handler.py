# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the ErrorHandler cog."""

from unittest.mock import AsyncMock, MagicMock

import discord
import pytest
from discord.ext import commands

from cogs.error_handler import ErrorHandler


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
