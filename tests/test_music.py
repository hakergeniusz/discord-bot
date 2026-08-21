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

"""Tests for the Music cog."""

from unittest.mock import AsyncMock, MagicMock

import discord
import pytest

from cogs.music import Music


def test_music_init() -> None:
    """Test Music cog initialization."""
    bot = MagicMock(spec=discord.ext.commands.Bot)
    cog = Music(bot)
    assert cog.bot == bot
    assert cog.queues == {}
    assert cog.current_song == {}


@pytest.mark.asyncio
async def test_nowplaying_empty() -> None:
    """Test nowplaying command when queue is empty."""
    ctx = AsyncMock()
    ctx.guild = MagicMock()
    ctx.guild.id = 123
    ctx.guild.voice_client = MagicMock()
    ctx.guild.voice_client.is_playing.return_value = False

    cog = Music(MagicMock())

    await cog.nowplaying.callback(cog, ctx)
    ctx.send.assert_called_with("Nothing is playing right now.")


@pytest.mark.asyncio
async def test_music_queue_empty() -> None:
    """Test queue command when queue is empty."""
    ctx = AsyncMock()
    ctx.guild.id = 123
    cog = Music(MagicMock())

    await cog.queue.callback(cog, ctx)
    ctx.send.assert_called_with("The queue is empty.")


@pytest.mark.asyncio
async def test_music_skip_nothing_playing() -> None:
    """Test skip command when nothing is playing."""
    ctx = AsyncMock()
    ctx.guild.voice_client = None
    cog = Music(MagicMock())

    await cog.skip.callback(cog, ctx)
    ctx.send.assert_called_with("Nothing is playing right now.")
