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
