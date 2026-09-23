# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Tests for Fun and F1 cogs."""

from unittest.mock import AsyncMock, MagicMock, patch

import discord
import pytest
from discord.ext import commands

from cogs.fun import F1Commands, HowManyButtonButtons, Meme


def test_f1_commands_init() -> None:
    """Test F1Commands initialization."""
    bot = MagicMock(spec=discord.ext.commands.Bot)
    cog = F1Commands(bot)
    assert cog.bot == bot


def test_meme_init() -> None:
    """Test Meme cog initialization."""
    bot = MagicMock(spec=discord.ext.commands.Bot)
    cog = Meme(bot)
    assert cog.bot == bot


@pytest.mark.asyncio
async def test_howmanybutton_button_callback() -> None:
    """Test howmanybutton button callback."""
    bot = MagicMock(spec=discord.ext.commands.Bot)
    view = HowManyButtonButtons(bot)
    interaction = AsyncMock(spec=discord.Interaction)
    interaction.user.id = 123
    interaction.user.mention = "<@123>"
    interaction.response = AsyncMock()

    # Mocking change_file since it's an external dependency
    with patch("cogs.fun.change_file", return_value=1):
        await view.howmanybutton_button.callback(interaction)

    interaction.response.edit_message.assert_called_once()
    edit_message = interaction.response.edit_message
    assert "<@123> clicked the button 1 time!" in edit_message.call_args.kwargs["content"]


@pytest.mark.asyncio
async def test_meme_heart() -> None:
    """Test Meme.heart command."""
    cog = Meme(MagicMock())
    ctx = AsyncMock(spec=commands.Context)

    await cog.heart.callback(cog, ctx)
    ctx.send.assert_called_with(":middle_finger:", ephemeral=True)


@pytest.mark.asyncio
async def test_meme_finger() -> None:
    """Test Meme.finger command."""
    cog = Meme(MagicMock())
    ctx = AsyncMock(spec=commands.Context)

    await cog.finger.callback(cog, ctx)
    ctx.send.assert_called_with(":heart:", ephemeral=True)


@pytest.mark.asyncio
async def test_meme_archbtw() -> None:
    """Test Meme.archbtw command."""
    cog = Meme(MagicMock())
    ctx = AsyncMock(spec=commands.Context)

    await cog.archbtw.callback(cog, ctx)
    ctx.reply.assert_called_with("I use Arch btw")
