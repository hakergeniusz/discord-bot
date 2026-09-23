# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the Other cog."""

from unittest.mock import AsyncMock, MagicMock

import discord
import pytest

from cogs.other import Other


def test_other_init() -> None:
    """Test Other cog initialization."""
    bot = MagicMock(spec=discord.ext.commands.Bot)
    cog = Other(bot)
    assert cog.bot == bot


@pytest.mark.asyncio
async def test_ping() -> None:
    """Test ping command."""
    ctx = AsyncMock()
    bot = MagicMock(spec=discord.ext.commands.Bot)
    bot.latency = 0.1
    cog = Other(bot)

    await cog.ping.callback(cog, ctx)
    ctx.reply.assert_called_with("Pong! Latency is 100ms")
