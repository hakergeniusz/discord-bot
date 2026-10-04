# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Tests for the Music cog."""

from unittest.mock import AsyncMock, MagicMock, patch

import discord
import pytest
from discord.ext import commands

from cogs.music import Music, Song, setup

_ERROR_MESSAGE = "boom"


def _make_song(requester_id: int = 456) -> Song:
    """Build a Song double.

    Args:
        requester_id: ID of the user who requested the song.

    Returns:
        Song: Song with fixed metadata.
    """
    return Song(
        path="/tmp/song.mp3",
        title="Test Song",
        duration="3:20",
        thumbnail="http://thumb.test/i.png",
        requester_id=requester_id,
        video_id="vid123",
        time_started=0,
    )


def _make_ctx(*, guild_id: int = 123, playing: bool = False) -> AsyncMock:
    """Build a Context double with a guild voice client.

    Args:
        guild_id: ID of the fake guild.
        playing: Value returned by ``voice_client.is_playing``.

    Returns:
        AsyncMock: Context double ready to be passed to a command callback.
    """
    ctx = AsyncMock()
    ctx.guild = MagicMock()
    ctx.guild.id = guild_id
    ctx.guild.voice_client = MagicMock(spec=discord.VoiceClient)
    ctx.guild.voice_client.is_playing.return_value = playing
    ctx.author = MagicMock()
    ctx.author.id = 456
    ctx.author.voice = MagicMock()
    ctx.author.voice.channel = AsyncMock()
    ctx.send.return_value = AsyncMock()
    return ctx


def _make_bot() -> MagicMock:
    """Build a Bot double with a loop.

    Returns:
        MagicMock: Bot double usable by the cog.
    """
    bot = MagicMock(spec=commands.Bot)
    bot.loop = MagicMock()
    return bot


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


@pytest.mark.asyncio
async def test_music_group_dm_lists_commands() -> None:
    """Test music group help text sent when invoked in a DM."""
    cog = Music(MagicMock())
    ctx = AsyncMock()
    ctx.invoked_subcommand = None
    ctx.guild = None

    await cog.music.callback(cog, ctx)

    sent = ctx.send.call_args.args[0]
    assert "Available commands" in sent


@pytest.mark.asyncio
async def test_music_group_in_guild_lists_commands() -> None:
    """Test music group help text sent from a guild."""
    cog = Music(MagicMock())
    ctx = AsyncMock()
    ctx.invoked_subcommand = None
    ctx.guild = MagicMock()

    await cog.music.callback(cog, ctx)

    ctx.send.assert_called_once_with("Available commands: play, skip, leave, queue, nowplaying.")


@pytest.mark.asyncio
async def test_music_group_with_subcommand_is_noop() -> None:
    """Test that the group does nothing when a subcommand was invoked."""
    cog = Music(MagicMock())
    ctx = AsyncMock()
    ctx.invoked_subcommand = MagicMock()

    await cog.music.callback(cog, ctx)

    ctx.send.assert_not_called()


@pytest.mark.asyncio
async def test_play_not_in_voice_channel() -> None:
    """Test play when the author is not connected to voice."""
    cog = Music(MagicMock())
    ctx = _make_ctx()
    ctx.author.voice = None

    await cog.play.callback(cog, ctx, "https://youtu.be/x")

    ctx.send.assert_called_with("You are not in a voice channel.")


@pytest.mark.asyncio
async def test_play_without_guild() -> None:
    """Test play aborting silently outside a guild."""
    cog = Music(MagicMock())
    ctx = _make_ctx()
    ctx.guild = None

    await cog.play.callback(cog, ctx, "https://youtu.be/x")

    ctx.send.assert_not_called()


@pytest.mark.asyncio
async def test_play_already_queued_as_non_admin() -> None:
    """Test play rejecting a second queued song from a non-admin."""
    cog = Music(MagicMock())
    cog.queues[123] = [_make_song()]
    ctx = _make_ctx()

    with patch("cogs.music.ADMINS", []):
        await cog.play.callback(cog, ctx, "https://youtu.be/x")

    ctx.send.assert_called_with("You already have a song in in the queue.")


@pytest.mark.asyncio
async def test_play_admin_may_queue_second_song() -> None:
    """Test play letting an admin queue another song while one plays."""
    cog = Music(MagicMock())
    queued = _make_song()
    cog.queues[123] = [queued]
    ctx = _make_ctx(playing=True)
    download = ("/tmp/a.mp3", "New Song", 200, "http://thumb.test/n.png", "vid999")

    with (
        patch("cogs.music.ADMINS", [456]),
        patch("cogs.music.download_youtube_video", return_value=download),
    ):
        await cog.play.callback(cog, ctx, "https://youtu.be/x")

    assert cog.queues[123][-1].title == "New Song"
    edit_kwargs = ctx.send.return_value.edit.call_args.kwargs
    assert not edit_kwargs["content"]
    assert edit_kwargs["embed"].title == "Added to queue"


@pytest.mark.asyncio
async def test_play_already_playing_own_song() -> None:
    """Test play rejecting a song from the author already playing."""
    cog = Music(MagicMock())
    cog.current_song[123] = _make_song()
    ctx = _make_ctx()

    await cog.play.callback(cog, ctx, "https://youtu.be/x")

    ctx.send.assert_called_with("A song submitted by you is already playing.")


@pytest.mark.asyncio
async def test_play_download_failure() -> None:
    """Test play reporting a failed download."""
    cog = Music(MagicMock())
    ctx = _make_ctx()

    with patch("cogs.music.download_youtube_video", return_value=(None, None, None, None, None)):
        await cog.play.callback(cog, ctx, "https://youtu.be/x")

    ctx.send.return_value.edit.assert_called_once_with(
        content="Incorrect URL/Failed to download video.",
    )


@pytest.mark.asyncio
async def test_play_moves_to_user_channel_and_plays() -> None:
    """Test play moving the bot to the author's channel and starting playback."""
    bot = _make_bot()
    cog = Music(bot)
    ctx = _make_ctx()
    download = ("/tmp/a.mp3", "New Song", 200, "http://thumb.test/n.png", "vid999")

    with (
        patch("cogs.music.download_youtube_video", return_value=download),
        patch("cogs.music.discord.FFmpegPCMAudio"),
    ):
        await cog.play.callback(cog, ctx, "https://youtu.be/x")

    ctx.guild.voice_client.move_to.assert_awaited_once_with(ctx.author.voice.channel)
    ctx.guild.voice_client.play.assert_called_once()
    assert cog.current_song[123].title == "New Song"
    ctx.channel.send.assert_awaited_once()
    embed = ctx.channel.send.call_args.kwargs["embed"]
    assert embed.title == "Starting playing"


@pytest.mark.asyncio
async def test_play_connects_when_bot_not_in_channel() -> None:
    """Test play connecting to the author's channel when the bot is idle."""
    cog = Music(MagicMock())
    ctx = _make_ctx()
    ctx.guild.voice_client = None
    download = ("/tmp/a.mp3", "New Song", 200, "http://thumb.test/n.png", "vid999")

    with (
        patch("cogs.music.download_youtube_video", return_value=download),
        patch("cogs.music.discord.FFmpegPCMAudio"),
    ):
        await cog.play.callback(cog, ctx, "https://youtu.be/x")

    ctx.author.voice.channel.connect.assert_awaited_once()
    ctx.send.return_value.edit.assert_called_once_with(content="Voice client not connected.")


@pytest.mark.asyncio
async def test_start_playback_audio_failure() -> None:
    """Test _start_playback reporting an audio failure."""
    cog = Music(MagicMock())
    ctx = _make_ctx()
    first_response = AsyncMock()
    ctx.guild.voice_client.play.side_effect = discord.DiscordException(
        MagicMock(status=500),
        _ERROR_MESSAGE,
    )

    with patch("cogs.music.discord.FFmpegPCMAudio"):
        await cog._start_playback(ctx, first_response, 123, _make_song(), "/tmp/a.mp3")

    first_response.edit.assert_awaited_once_with(content="Failed to play audio.")
    assert cog.current_song[123] is None


@pytest.mark.asyncio
async def test_play_next_with_empty_queue() -> None:
    """Test _play_next clearing the current song when the queue is drained."""
    cog = Music(MagicMock())
    cog.current_song[123] = _make_song()

    await cog._play_next(123, AsyncMock())

    assert cog.current_song[123] is None


@pytest.mark.asyncio
async def test_play_next_without_voice_client() -> None:
    """Test _play_next leaving the queue untouched without a voice client."""
    cog = Music(MagicMock())
    song = _make_song()
    cog.queues[123] = [song]
    interaction = AsyncMock()
    interaction.guild.voice_client = None

    await cog._play_next(123, interaction)

    assert cog.queues[123] == [song]


@pytest.mark.asyncio
async def test_play_next_pops_song_and_chains_callback() -> None:
    """Test _play_next starting playback and chaining the after callback."""
    bot = _make_bot()
    cog = Music(bot)
    song = _make_song()
    cog.queues[123] = [song]
    interaction = AsyncMock()
    interaction.guild.voice_client = MagicMock(spec=discord.VoiceClient)

    with patch("cogs.music.discord.FFmpegPCMAudio"):
        await cog._play_next(123, interaction)

    assert cog.queues[123] == []
    assert cog.current_song[123] is song
    interaction.guild.voice_client.play.assert_called_once()
    after = interaction.guild.voice_client.play.call_args.kwargs["after"]
    after(None)
    bot.loop.call_soon_threadsafe.assert_called_once()


@pytest.mark.asyncio
async def test_play_next_audio_failure_is_logged() -> None:
    """Test _play_next swallowing an audio failure."""
    cog = Music(MagicMock())
    song = _make_song()
    cog.queues[123] = [song]
    interaction = AsyncMock()
    interaction.guild.voice_client = MagicMock(spec=discord.VoiceClient)
    interaction.guild.voice_client.play.side_effect = discord.DiscordException(
        MagicMock(status=500),
        _ERROR_MESSAGE,
    )

    with patch("cogs.music.discord.FFmpegPCMAudio"):
        await cog._play_next(123, interaction)

    interaction.channel.send.assert_not_awaited()


@pytest.mark.asyncio
async def test_send_now_playing_embed_without_thumbnail() -> None:
    """Test the now playing embed skipping the thumbnail when absent."""
    interaction = AsyncMock()
    song = _make_song()
    song.thumbnail = ""

    await Music._send_now_playing_embed(interaction, song)

    embed = interaction.channel.send.call_args.kwargs["embed"]
    assert embed.thumbnail.url is None
    assert song.time_started > 0


@pytest.mark.asyncio
async def test_leave_when_bot_not_connected() -> None:
    """Test leave when the bot has no voice client."""
    cog = Music(MagicMock())
    ctx = _make_ctx()
    ctx.guild.voice_client = None

    await cog.leave.callback(cog, ctx)

    ctx.send.assert_called_once_with("I'm not in a voice channel.", ephemeral=True)


@pytest.mark.asyncio
async def test_leave_disconnects_and_clears_queue() -> None:
    """Test leave disconnecting and clearing per-guild state."""
    cog = Music(MagicMock())
    cog.queues[123] = [_make_song()]
    cog.current_song[123] = _make_song()
    ctx = _make_ctx()

    await cog.leave.callback(cog, ctx)

    assert cog.queues[123] == []
    assert cog.current_song[123] is None
    ctx.guild.voice_client.disconnect.assert_awaited_once()
    ctx.send.assert_called_once_with("Left the voice channel.")


@pytest.mark.asyncio
async def test_leave_forbidden() -> None:
    """Test leave reporting a missing permission."""
    cog = Music(MagicMock())
    ctx = _make_ctx()
    ctx.guild.voice_client.disconnect.side_effect = discord.Forbidden(
        MagicMock(status=403),
        _ERROR_MESSAGE,
    )

    await cog.leave.callback(cog, ctx)

    ctx.send.assert_called_once_with("Failed to leave the voice channel.", ephemeral=True)


@pytest.mark.asyncio
async def test_queue_lists_songs() -> None:
    """Test queue rendering the queued songs."""
    cog = Music(MagicMock())
    cog.queues[123] = [_make_song(), _make_song(requester_id=999)]
    ctx = _make_ctx()

    await cog.queue.callback(cog, ctx)

    embed = ctx.send.call_args.kwargs["embed"]
    assert embed.title == "Music Queue"
    assert "**1. Test Song**" in embed.description
    assert "<@999>" in embed.description


@pytest.mark.asyncio
async def test_skip_stops_playback() -> None:
    """Test skip stopping the playing song."""
    cog = Music(MagicMock())
    ctx = _make_ctx(playing=True)

    await cog.skip.callback(cog, ctx)

    ctx.guild.voice_client.stop.assert_called_once()
    ctx.send.assert_called_once_with("Skipped the current song.")


@pytest.mark.asyncio
async def test_nowplaying_shows_song() -> None:
    """Test nowplaying rendering the currently playing song."""
    cog = Music(MagicMock())
    song = _make_song()
    song.time_started = 1
    cog.current_song[123] = song
    ctx = _make_ctx(playing=True)

    with patch("cogs.music.format_duration", return_value="1:05"):
        await cog.nowplaying.callback(cog, ctx)

    embed = ctx.send.call_args.kwargs["embed"]
    assert embed.title == "Now Playing"
    assert "Currently at" in embed.to_dict()["fields"][0]["name"]


@pytest.mark.asyncio
async def test_nowplaying_without_current_song() -> None:
    """Test nowplaying when nothing is tracked for the guild."""
    cog = Music(MagicMock())
    ctx = _make_ctx(playing=True)

    await cog.nowplaying.callback(cog, ctx)

    ctx.send.assert_called_once_with("Nothing is playing right now.")


@pytest.mark.asyncio
async def test_music_setup_adds_cog() -> None:
    """Test that setup registers the Music cog."""
    bot = MagicMock(spec=commands.Bot)
    bot.add_cog = AsyncMock()

    await setup(bot)

    bot.add_cog.assert_awaited_once()
    assert isinstance(bot.add_cog.call_args.args[0], Music)
