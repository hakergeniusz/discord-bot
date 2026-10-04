# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the Utility cog."""

from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, MagicMock, patch

import discord
import pytest
from discord.ext import commands

from core.config import AI_RESPONSE_LIMIT

# core.ai builds a Gemini client at import time, which needs an API key that CI
# does not provide. Every test below replaces process_prompt anyway.
with patch("google.genai.Client"):
    from cogs.utility import Utility, setup

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Callable
    from pathlib import Path

WEBHOOK_URL = "https://discord.com/api/webhooks/123/abc"
LONG_ANSWER = "z" * (AI_RESPONSE_LIMIT + 500)


def _chunk_stream(*chunks: str) -> Callable[[str], AsyncIterator[str]]:
    """Build a stand-in for ``process_prompt`` yielding canned chunks.

    Args:
        chunks: Chunks yielded by the fake generator.

    Returns:
        Callable: Replacement for ``core.ai.process_prompt``.
    """

    async def stream(_: str) -> AsyncIterator[str]:
        """Yield the canned chunks.

        Args:
            _: Prompt, ignored by the fake generator.

        Yields:
            str: The canned chunks.
        """
        for chunk in chunks:
            yield chunk

    return stream


def _dir_is_empty(path: Path) -> bool:
    """Return whether a directory holds no entries.

    Args:
        path: Directory to inspect.

    Returns:
        bool: True when the directory is empty.
    """
    return not any(path.iterdir())


@pytest.fixture
def answer_file(tmp_path: Path) -> Path:
    """Write a pre-made answer file where the AI command expects it.

    Args:
        tmp_path: pytest-provided temporary directory.

    Returns:
        Path: Path of the created file.
    """
    file_path = tmp_path / "100000.txt"
    file_path.write_text(LONG_ANSWER, encoding="utf-8")
    return file_path


def _make_bot() -> MagicMock:
    """Build a Bot double.

    Returns:
        MagicMock: Bot double whose fetch_channel is awaitable.
    """
    bot = MagicMock(spec=commands.Bot)
    bot.fetch_channel = AsyncMock(return_value=AsyncMock())
    return bot


def _make_interaction() -> AsyncMock:
    """Build an Interaction double.

    Returns:
        AsyncMock: Interaction double ready for command callbacks.
    """
    interaction = AsyncMock(spec=discord.Interaction)
    interaction.response = AsyncMock()
    interaction.followup = AsyncMock()
    interaction.edit_original_response = AsyncMock()
    return interaction


def _make_session(
    get_status: int = 204,
    post_status: int = 204,
) -> MagicMock:
    """Build an aiohttp session double with async context manager support.

    Args:
        get_status: Status returned by the GET request.
        post_status: Status returned by the POST request.

    Returns:
        MagicMock: Session double usable with ``async with``.
    """
    session = MagicMock()
    session.__aenter__.return_value = session
    session.__aexit__.return_value = False

    get_response = MagicMock()
    get_response.status = get_status
    session.get.return_value.__aenter__.return_value = get_response

    post_response = MagicMock()
    post_response.status = post_status
    session.post.return_value.__aenter__.return_value = post_response

    return session


def test_utility_init() -> None:
    """Test Utility cog initialization."""
    bot = MagicMock(spec=commands.Bot)
    cog = Utility(bot)
    assert cog.bot == bot


@pytest.mark.asyncio
async def test_webhook_rejects_bad_url() -> None:
    """Test webhook rejecting a URL outside Discord."""
    cog = Utility(_make_bot())
    interaction = _make_interaction()

    await cog.webhook.callback(cog, interaction, "https://example.com/hook", "hi")

    interaction.followup.send.assert_awaited_once_with("Invalid webhook URL.", ephemeral=True)


@pytest.mark.asyncio
async def test_webhook_upgrades_scheme_and_host() -> None:
    """Test webhook normalising http and host-less webhook URLs."""
    cog = Utility(_make_bot())
    interaction = _make_interaction()
    session = _make_session()

    with (
        patch("cogs.utility.aiohttp.ClientSession", return_value=session),
        patch("cogs.utility.image_checker", new=AsyncMock(return_value=True)),
    ):
        await cog.webhook.callback(
            cog,
            interaction,
            "discord.com/api/webhooks/123/abc",
            "hi",
            name="Bot",
            avatar_url="http://avatar.test/a.png",
        )

    assert session.get.call_args.args[0] == WEBHOOK_URL
    assert session.post.call_args.args[0] == WEBHOOK_URL
    assert session.post.call_args.kwargs["json"] == {
        "content": "hi",
        "username": "Bot",
        "avatar_url": "http://avatar.test/a.png",
    }
    interaction.followup.send.assert_awaited_with("Message sent successfully.", ephemeral=True)


@pytest.mark.asyncio
async def test_webhook_unauthorized() -> None:
    """Test webhook handling a 401 response."""
    cog = Utility(_make_bot())
    interaction = _make_interaction()
    session = _make_session(get_status=401)

    with patch("cogs.utility.aiohttp.ClientSession", return_value=session):
        await cog.webhook.callback(cog, interaction, WEBHOOK_URL, "hi")

    session.post.assert_not_called()
    interaction.followup.send.assert_awaited_once_with("Invalid webhook URL.", ephemeral=True)


@pytest.mark.asyncio
async def test_webhook_rate_limited() -> None:
    """Test webhook handling a 429 response."""
    cog = Utility(_make_bot())
    interaction = _make_interaction()
    session = _make_session(post_status=429)

    with patch("cogs.utility.aiohttp.ClientSession", return_value=session):
        await cog.webhook.callback(cog, interaction, WEBHOOK_URL, "hi")

    interaction.followup.send.assert_awaited_once_with("Rate-limit has been hit. ", ephemeral=True)


@pytest.mark.asyncio
async def test_webhook_rejects_bad_avatar() -> None:
    """Test webhook rejecting an avatar URL that is not an image."""
    cog = Utility(_make_bot())
    interaction = _make_interaction()
    session = _make_session()

    with (
        patch("cogs.utility.aiohttp.ClientSession", return_value=session),
        patch("cogs.utility.image_checker", new=AsyncMock(return_value=False)),
    ):
        await cog.webhook.callback(
            cog,
            interaction,
            WEBHOOK_URL,
            "hi",
            avatar_url="http://avatar.test/nope.png",
        )

    session.post.assert_not_called()
    interaction.followup.send.assert_awaited_once_with("Incorrect avatar URL.", ephemeral=True)


@pytest.mark.asyncio
async def test_say_sends_message() -> None:
    """Test say sending a message through a fetched channel."""
    bot = _make_bot()
    cog = Utility(bot)
    interaction = _make_interaction()
    interaction.channel_id = 555

    await cog.say.callback(cog, interaction, "hello")

    bot.fetch_channel.assert_awaited_once_with(555)
    bot.fetch_channel.return_value.send.assert_awaited_once_with("hello")
    interaction.response.send_message.assert_awaited_once_with(
        "Message sent to <#555>",
        ephemeral=True,
    )
    bot.fetch_channel.return_value.send.return_value.delete.assert_not_awaited()


@pytest.mark.asyncio
async def test_say_deletes_after_delay() -> None:
    """Test say removing the message after delete_after seconds."""
    bot = _make_bot()
    cog = Utility(bot)
    interaction = _make_interaction()
    interaction.channel_id = 555
    message = AsyncMock()
    bot.fetch_channel.return_value.send.return_value = message

    with patch("cogs.utility.asyncio.sleep", new=AsyncMock()) as sleep:
        await cog.say.callback(cog, interaction, "hello", 5)

    sleep.assert_awaited_once_with(5)
    message.delete.assert_awaited_once()
    interaction.edit_original_response.assert_awaited_once()
    assert (
        "was removed due to request"
        in interaction.edit_original_response.call_args.kwargs["content"]
    )


@pytest.mark.asyncio
async def test_dm_or_not_in_guild() -> None:
    """Test dm_or_not inside a guild."""
    cog = Utility(_make_bot())
    ctx = AsyncMock(spec=commands.Context)
    ctx.guild = MagicMock()

    await cog.dmornot.callback(cog, ctx)

    ctx.send.assert_awaited_once_with("It is a server")


@pytest.mark.asyncio
async def test_dm_or_not_in_dm() -> None:
    """Test dm_or_not outside a guild."""
    cog = Utility(_make_bot())
    ctx = AsyncMock(spec=commands.Context)
    ctx.guild = None

    await cog.dmornot.callback(cog, ctx)

    ctx.send.assert_awaited_once_with("It is a DM")


@pytest.mark.asyncio
async def test_ai_short_response() -> None:
    """Test ai editing the placeholder message with a short answer."""
    cog = Utility(_make_bot())
    ctx = AsyncMock(spec=commands.Context)
    ctx.send.return_value = AsyncMock()

    with patch("cogs.utility.process_prompt", new=_chunk_stream("Hello", " ", "world")):
        await cog.ai.callback(cog, ctx, prompt="hi")

    ctx.defer.assert_awaited_once()
    ctx.send.assert_awaited_once_with("▌")
    ctx.send.return_value.edit.assert_awaited_with(content="Hello world")


@pytest.mark.asyncio
async def test_ai_long_response_warns_about_limit() -> None:
    """Test ai warning the user when the answer crosses the message limit."""
    cog = Utility(_make_bot())
    ctx = AsyncMock(spec=commands.Context)
    ctx.send.return_value = AsyncMock()
    chunks = ("x" * 1000, "y" * (AI_RESPONSE_LIMIT - 1000 + 5))

    with (
        patch("cogs.utility.process_prompt", new=_chunk_stream(*chunks)),
        patch("cogs.utility.create_file", new=AsyncMock(return_value=None)),
    ):
        await cog.ai.callback(cog, ctx, prompt="hi")

    warned = [
        call
        for call in ctx.send.return_value.edit.await_args_list
        if "Soon, file with full response will be provided." in call.kwargs["content"]
    ]
    assert len(warned) == 1


@pytest.mark.asyncio
async def test_ai_long_response_sends_file(tmp_path: Path, answer_file: Path) -> None:
    """Test ai attaching the full answer as a file when it is too long."""
    assert answer_file.parent == tmp_path
    cog = Utility(_make_bot())
    ctx = AsyncMock(spec=commands.Context)
    ctx.send.return_value = AsyncMock()

    with (
        patch("cogs.utility.TMP_BASE", tmp_path),
        patch("cogs.utility.secrets.randbelow", return_value=0),
        patch("cogs.utility.process_prompt", new=_chunk_stream(LONG_ANSWER)),
        patch("cogs.utility.create_file", new=AsyncMock(return_value=True)),
        patch("cogs.utility.asyncio.sleep", new=AsyncMock()),
    ):
        await cog.ai.callback(cog, ctx, prompt="hi")

    send_kwargs = ctx.send.call_args.kwargs
    assert send_kwargs["content"] == "Here is the file with the full response:"
    assert isinstance(send_kwargs["file"], discord.File)
    ctx.send.return_value.delete.assert_awaited_once()
    assert _dir_is_empty(tmp_path)


@pytest.mark.asyncio
async def test_ai_long_response_missing_file(tmp_path: Path) -> None:
    """Test ai reporting a failure to write the answer file."""
    cog = Utility(_make_bot())
    ctx = AsyncMock(spec=commands.Context)
    ctx.send.return_value = AsyncMock()

    with (
        patch("cogs.utility.TMP_BASE", tmp_path),
        patch("cogs.utility.process_prompt", new=_chunk_stream(LONG_ANSWER)),
        patch("cogs.utility.create_file", new=AsyncMock(return_value=None)),
        patch("cogs.utility.asyncio.sleep", new=AsyncMock()),
    ):
        await cog.ai.callback(cog, ctx, prompt="hi")

    assert "Error while making a file" in ctx.send.return_value.edit.call_args.kwargs["content"]


@pytest.mark.asyncio
async def test_hide_sends_padding() -> None:
    """Test hide sending the padded message."""
    cog = Utility(_make_bot())
    ctx = AsyncMock(spec=commands.Context)

    await cog.hide.callback(cog, ctx)

    sent = ctx.send.call_args.args[0]
    assert sent.startswith("e")
    assert sent.endswith("e")
    assert len(sent) > 100


@pytest.mark.asyncio
async def test_on_message_listener_is_noop() -> None:
    """Test that the on_message listener does nothing."""
    cog = Utility(_make_bot())

    assert await cog.on_message(AsyncMock(spec=discord.Message)) is None


@pytest.mark.asyncio
async def test_utility_setup_adds_cog() -> None:
    """Test that setup registers the Utility cog."""
    bot = MagicMock(spec=commands.Bot)
    bot.add_cog = AsyncMock()

    await setup(bot)

    bot.add_cog.assert_awaited_once()
    assert isinstance(bot.add_cog.call_args.args[0], Utility)
