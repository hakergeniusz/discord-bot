# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the Other cog."""

from unittest.mock import AsyncMock, MagicMock

import discord
import pytest

from cogs.other import Other, setup


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


@pytest.mark.asyncio
async def test_ping_rounds_latency() -> None:
    """Test ping rounding the latency to whole milliseconds."""
    bot = MagicMock(spec=discord.ext.commands.Bot)
    bot.latency = 0.01234
    cog = Other(bot)
    ctx = AsyncMock()

    await cog.ping.callback(cog, ctx)

    ctx.reply.assert_called_with("Pong! Latency is 12ms")


@pytest.mark.asyncio
async def test_source_without_interaction() -> None:
    """Test source sending a plain link outside an interaction."""
    cog = Other(MagicMock(spec=discord.ext.commands.Bot))
    ctx = AsyncMock()
    ctx.interaction = None

    await cog.source.callback(cog, ctx)

    assert "https://github.com/hakergeniusz/discord-bot" in ctx.send.call_args.args[0]


@pytest.mark.asyncio
async def test_source_with_interaction() -> None:
    """Test source sending a button view inside an interaction."""
    cog = Other(MagicMock(spec=discord.ext.commands.Bot))
    ctx = AsyncMock()
    ctx.interaction = AsyncMock()

    await cog.source.callback(cog, ctx)

    view = ctx.send.call_args.kwargs["view"]
    assert view.children[0].url == "https://github.com/hakergeniusz/discord-bot"


@pytest.mark.asyncio
async def test_licence_without_interaction() -> None:
    """Test licence sending plain text outside an interaction."""
    cog = Other(MagicMock(spec=discord.ext.commands.Bot))
    ctx = AsyncMock()
    ctx.interaction = None

    await cog.licence.callback(cog, ctx)

    sent = ctx.send.call_args.args[0]
    assert "EUPL-1.2" in sent
    assert "embed" not in ctx.send.call_args.kwargs


@pytest.mark.asyncio
async def test_licence_with_interaction() -> None:
    """Test licence sending an embed and button view inside an interaction."""
    cog = Other(MagicMock(spec=discord.ext.commands.Bot))
    ctx = AsyncMock()
    ctx.interaction = AsyncMock()

    await cog.licence.callback(cog, ctx)

    kwargs = ctx.send.call_args.kwargs
    assert kwargs["embed"].title == "📜 Legal Information & License"
    assert len(kwargs["view"].children) == 1


@pytest.mark.asyncio
async def test_other_setup_adds_cog() -> None:
    """Test that setup registers the Other cog."""
    bot = MagicMock(spec=discord.ext.commands.Bot)
    bot.add_cog = AsyncMock()

    await setup(bot)

    bot.add_cog.assert_awaited_once()
    assert isinstance(bot.add_cog.call_args.args[0], Other)
