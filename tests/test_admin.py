# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the Admin cog."""

from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import discord
import pytest
from discord.ext import commands

from cogs.admin import AdminCommands, StatusButtons, setup

_ERROR_MESSAGE = "boom"


def _make_ctx() -> AsyncMock:
    """Build a Context double with channel permissions.

    Returns:
        AsyncMock: Context double ready for command callbacks.
    """
    ctx = AsyncMock(spec=commands.Context)
    ctx.permissions.manage_messages = True
    ctx.interaction = None
    ctx.message = AsyncMock()
    ctx.channel.purge = AsyncMock()
    ctx.send.return_value = AsyncMock()
    return ctx


def _make_session(status: int) -> MagicMock:
    """Build an aiohttp session double returning a fixed status.

    Args:
        status: Status code reported by the DELETE response.

    Returns:
        MagicMock: Session double usable with ``async with``.
    """
    session = MagicMock()
    session.__aenter__.return_value = session
    session.__aexit__.return_value = False
    response = MagicMock()
    response.status = status
    session.delete.return_value.__aenter__.return_value = response
    return session


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


@pytest.mark.asyncio
async def test_status_buttons_dnd() -> None:
    """Test setting the bot status to do not disturb."""
    bot = MagicMock(spec=commands.Bot)
    bot.change_presence = AsyncMock()
    view = StatusButtons(bot)
    interaction = AsyncMock(spec=discord.Interaction)
    interaction.response = AsyncMock()

    await view.dnd_button.callback(interaction)

    assert bot.change_presence.call_args.kwargs["status"] == discord.Status.dnd


@pytest.mark.asyncio
async def test_status_buttons_idle() -> None:
    """Test setting the bot status to idle."""
    bot = MagicMock(spec=commands.Bot)
    bot.change_presence = AsyncMock()
    view = StatusButtons(bot)
    interaction = AsyncMock(spec=discord.Interaction)
    interaction.response = AsyncMock()

    await view.idle_button.callback(interaction)

    assert bot.change_presence.call_args.kwargs["status"] == discord.Status.idle


@pytest.mark.asyncio
async def test_status_buttons_invisible() -> None:
    """Test setting the bot status to invisible."""
    bot = MagicMock(spec=commands.Bot)
    bot.change_presence = AsyncMock()
    view = StatusButtons(bot)
    interaction = AsyncMock(spec=discord.Interaction)
    interaction.response = AsyncMock()

    await view.invisible_button.callback(interaction)

    assert bot.change_presence.call_args.kwargs["status"] == discord.Status.invisible
    interaction.response.send_message.assert_awaited_once_with(
        "Status set to Invisible",
        ephemeral=True,
    )


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


@pytest.mark.asyncio
async def test_create_webhook_forbidden() -> None:
    """Test create_webhook reporting a missing permission."""
    cog = AdminCommands(MagicMock())
    ctx = AsyncMock(spec=commands.Context)
    ctx.channel.create_webhook = AsyncMock()
    ctx.channel.create_webhook.side_effect = discord.Forbidden(
        MagicMock(status=403),
        _ERROR_MESSAGE,
    )

    await cog.create_webhook.callback(cog, ctx)

    ctx.send.assert_called_once_with(
        "I am forbidden to create a webhook in this channel (I don't have permissions).",
    )


@pytest.mark.asyncio
async def test_create_webhook_client_error() -> None:
    """Test create_webhook reporting a network failure."""
    cog = AdminCommands(MagicMock())
    ctx = AsyncMock(spec=commands.Context)
    ctx.channel.create_webhook = AsyncMock()
    ctx.channel.create_webhook.side_effect = aiohttp.ClientError(_ERROR_MESSAGE)

    await cog.create_webhook.callback(cog, ctx)

    ctx.send.assert_called_once_with("Failed to create webhook.")


@pytest.mark.asyncio
async def test_change_status_sends_buttons() -> None:
    """Test change_status sending the status button view."""
    cog = AdminCommands(MagicMock())
    interaction = AsyncMock(spec=discord.Interaction)
    interaction.response = AsyncMock()

    await cog.change_status.callback(cog, interaction)

    view = interaction.response.send_message.call_args.kwargs["view"]
    assert isinstance(view, StatusButtons)


@pytest.mark.asyncio
async def test_delete_webhook_success() -> None:
    """Test delete_webhook on a 204 response."""
    cog = AdminCommands(MagicMock())
    ctx = AsyncMock(spec=commands.Context)

    with patch("cogs.admin.aiohttp.ClientSession", return_value=_make_session(204)):
        await cog.delete_webhook.callback(cog, ctx, "https://discord.com/api/webhooks/1/x")

    ctx.send.assert_called_once_with("Removed webhook successfully")


@pytest.mark.asyncio
async def test_delete_webhook_missing() -> None:
    """Test delete_webhook on a 404 response."""
    cog = AdminCommands(MagicMock())
    ctx = AsyncMock(spec=commands.Context)

    with patch("cogs.admin.aiohttp.ClientSession", return_value=_make_session(404)):
        await cog.delete_webhook.callback(cog, ctx, "https://discord.com/api/webhooks/1/x")

    ctx.send.assert_called_once_with(
        "This webhook does not exist. You may have already deleted it.",
    )


@pytest.mark.asyncio
async def test_delete_webhook_unknown_status() -> None:
    """Test delete_webhook on an unexpected status code."""
    cog = AdminCommands(MagicMock())
    ctx = AsyncMock(spec=commands.Context)

    with patch("cogs.admin.aiohttp.ClientSession", return_value=_make_session(500)):
        await cog.delete_webhook.callback(cog, ctx, "https://discord.com/api/webhooks/1/x")

    assert "Response code is 500" in ctx.send.call_args.args[0]


@pytest.mark.asyncio
async def test_purge_without_permission() -> None:
    """Test purge aborting when the bot lacks manage_messages."""
    cog = AdminCommands(MagicMock())
    ctx = _make_ctx()
    ctx.permissions.manage_messages = False

    await cog.purge.callback(cog, ctx, 5)

    ctx.channel.purge.assert_not_awaited()
    ctx.send.assert_called_once_with("I don't have necessary permissions to do that.")


@pytest.mark.asyncio
async def test_purge_without_triggering_message() -> None:
    """Test purge when there is no message to delete."""
    cog = AdminCommands(MagicMock())
    ctx = _make_ctx()
    ctx.message = None

    with patch("cogs.admin.asyncio.sleep", new=AsyncMock()):
        await cog.purge.callback(cog, ctx, 3)

    ctx.channel.purge.assert_awaited_once_with(limit=3)
    ctx.send.assert_awaited_once_with("Deleted 3 messages successfully.")


@pytest.mark.asyncio
async def test_purge_via_interaction() -> None:
    """Test purge replying through the interaction when invoked as a slash command."""
    cog = AdminCommands(MagicMock())
    ctx = _make_ctx()
    ctx.interaction = AsyncMock()
    ctx.message = None

    with patch("cogs.admin.asyncio.sleep", new=AsyncMock()):
        await cog.purge.callback(cog, ctx, 7)

    ctx.defer.assert_awaited_once_with(ephemeral=True)
    ctx.channel.purge.assert_awaited_once_with(limit=7)
    ctx.reply.assert_awaited_once_with("Deleted 7 messages successfully.")


@pytest.mark.asyncio
async def test_purge_survives_delete_failure() -> None:
    """Test purge swallowing a failure while deleting its reply."""
    cog = AdminCommands(MagicMock())
    ctx = _make_ctx()
    ctx.message = None
    ctx.send.return_value.delete.side_effect = discord.Forbidden(
        MagicMock(status=403),
        _ERROR_MESSAGE,
    )

    with patch("cogs.admin.asyncio.sleep", new=AsyncMock()):
        await cog.purge.callback(cog, ctx, 2)

    ctx.channel.purge.assert_awaited_once_with(limit=2)


@pytest.mark.asyncio
async def test_admin_setup_adds_cog() -> None:
    """Test that setup registers the AdminCommands cog."""
    bot = MagicMock(spec=commands.Bot)
    bot.add_cog = AsyncMock()

    await setup(bot)

    bot.add_cog.assert_awaited_once()
    assert isinstance(bot.add_cog.call_args.args[0], AdminCommands)
