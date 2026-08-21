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

"""Tests for the Admin cog."""

from unittest.mock import AsyncMock, MagicMock, patch

import discord
import pytest
from discord.ext import commands

from cogs.admin import AdminCommands, StatusButtons


@pytest.mark.asyncio
async def test_status_buttons_online() -> None:
    """Test setting the bot status to online."""
    bot = MagicMock(spec=commands.Bot)
    bot.change_presence = AsyncMock()
    view = StatusButtons(bot)
    interaction = AsyncMock(spec=discord.Interaction)
    interaction.response = AsyncMock()

    await view.online_button.callback(interaction)

    bot.change_presence.assert_called_once()
    assert bot.change_presence.call_args.kwargs["status"] == discord.Status.online
    interaction.response.send_message.assert_called_once()


def test_admin_commands_init() -> None:
    """Test initialization of AdminCommands cog."""
    bot = MagicMock(spec=commands.Bot)
    cog = AdminCommands(bot)
    assert cog.bot == bot


@pytest.mark.asyncio
async def test_shutdown() -> None:
    """Test shutdown command."""
    bot = AsyncMock(spec=commands.Bot)
    cog = AdminCommands(bot)
    ctx = AsyncMock(spec=commands.Context)

    await cog.shutdown.callback(cog, ctx)

    ctx.send.assert_called_once_with("Shutting down the bot...")
    bot.close.assert_called_once()


@pytest.mark.asyncio
async def test_purge_success() -> None:
    """Test successful purge command."""
    bot = MagicMock(spec=commands.Bot)
    cog = AdminCommands(bot)
    ctx = AsyncMock(spec=commands.Context)
    ctx.permissions.manage_messages = True
    ctx.interaction = None
    ctx.message = AsyncMock()
    ctx.channel.purge = AsyncMock()

    with patch("asyncio.sleep", return_value=None):
        await cog.purge.callback(cog, ctx, 10)

    ctx.message.delete.assert_called_once()
    ctx.channel.purge.assert_called_once_with(limit=10)
    ctx.send.assert_called_with("Deleted 10 messages successfully.")


@pytest.mark.asyncio
async def test_create_webhook_success() -> None:
    """Test successful webhook creation."""
    bot = MagicMock(spec=commands.Bot)
    cog = AdminCommands(bot)
    ctx = AsyncMock(spec=commands.Context)
    ctx.channel.create_webhook = AsyncMock()
    ctx.channel.create_webhook.return_value.url = "https://discord.com/api/webhooks/123"

    await cog.create_webhook.callback(cog, ctx)

    ctx.channel.create_webhook.assert_called_once_with(name="Test webhook")
    ctx.send.assert_called_once_with("https://discord.com/api/webhooks/123", ephemeral=True)
