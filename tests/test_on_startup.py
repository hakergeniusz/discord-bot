# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the on_startup cog."""

from unittest.mock import AsyncMock, MagicMock

import discord
import pytest
from discord.ext import commands

from cogs.on_startup import SyncCog


@pytest.mark.asyncio
async def test_on_ready_sync() -> None:
    """Test on_ready synchronization."""
    bot = MagicMock(spec=commands.Bot)
    bot.tree = AsyncMock()
    bot.change_presence = AsyncMock()
    cog = SyncCog(bot)

    await cog.on_ready()

    bot.tree.sync.assert_called_once()
    bot.change_presence.assert_called_once()
    _args, kwargs = bot.change_presence.call_args
    assert kwargs["status"] == discord.Status.dnd
