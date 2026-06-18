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

"""Module for music-related commands using YouTube."""

import asyncio
import sys
import time
from dataclasses import dataclass

import discord
from discord import app_commands
from discord.ext import commands

from core.admin_check import admin_check
from core.config import ADMINS
from core.logger import get_logger
from core.youtube import download_youtube_video, format_duration

logger = get_logger(__name__)


@dataclass
class Song:
    """Class to store song information."""

    path: str
    title: str
    duration: str
    thumbnail: str
    requester_id: int
    video_id: str
    time_started: int


class Music(commands.Cog):
    """Cog for playing music from YouTube."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the Music cog."""
        self.bot = bot
        self.queues = {}
        self.current_song = {}

    async def _play_next(
        self,
        guild_id: int,
        interaction: discord.Interaction | commands.Context,
    ) -> None:
        """Plays the next song in the queue for a guild."""
        if guild_id not in self.queues or not self.queues[guild_id]:
            self.current_song[guild_id] = None
            return

        if not interaction.guild:
            return

        vc_chan = interaction.guild.voice_client
        if not vc_chan or not isinstance(vc_chan, discord.VoiceClient):
            return

        song = self.queues[guild_id].pop(0)
        self.current_song[guild_id] = song
        try:
            ffmpeg_options = {"executable": "ffmpeg.exe"} if sys.platform == "win32" else {}
            music = discord.FFmpegPCMAudio(song.path, **ffmpeg_options)
            vc_chan.play(
                music,
                after=lambda _: self.bot.loop.call_soon_threadsafe(
                    lambda: asyncio.create_task(self._play_next(guild_id, interaction)),
                ),
            )
            yt_url = f"https://www.youtube.com/watch?v={song.video_id}"
            embed = discord.Embed(
                title="Starting playing",
                description=f"**[{song.title}]({yt_url})**",
                color=discord.Color.blue(),
            )
            embed.add_field(name="Duration", value=song.duration, inline=True)
            embed.add_field(
                name="Requested by",
                value=f"<@{song.requester_id}>",
                inline=True,
            )
            if song.thumbnail:
                embed.set_thumbnail(url=song.thumbnail)
            await interaction.channel.send(embed=embed)
            song.time_started = int(time.time())
        except discord.DiscordException, OSError:
            logger.exception("Failed to play audio")

    @commands.hybrid_group(name="music", invoke_without_command=True)
    async def music(self, ctx: commands.Context) -> None:
        """Default command used to group other ones."""
        if ctx.invoked_subcommand is None:
            await ctx.send("""
                Available commands: play, skip, leave, queue, nowplaying.
                > You can't use music commands in DMs anyway!
            """)

    @commands.guild_only()
    @music.command(name="play", description="Plays music on a voice channel")
    @app_commands.describe(youtube_url="Youtube URL of the video you want to play.")
    async def play(
        self,
        ctx: commands.Context,
        youtube_url: str = "https://www.youtube.com/watch?v=fpQHabt6e-w",
    ) -> None:
        """Plays music from a YouTube URL in a voice channel."""
        await ctx.defer()
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("You are not in a voice channel.")
            return

        if not ctx.guild:
            return

        vc_chan = ctx.guild.voice_client
        guild_id = ctx.guild.id
        queue = self.queues.get(guild_id, [])
        is_already_in_queue = any(s.requester_id == ctx.author.id for s in queue)
        if is_already_in_queue and ctx.author.id not in ADMINS:
            await ctx.send("You already have a song in in the queue.")
            return

        current = self.current_song.get(guild_id)

        if current and current.requester_id == ctx.author.id:
            await ctx.send("A song submitted by you is already playing.")
            return

        first_response = await ctx.send("Processing the video URL...")
        result = await asyncio.to_thread(download_youtube_video, youtube_url)

        if not result or result[0] is None:
            await first_response.edit(content="Incorrect URL/Failed to download video.")
            return

        path, title, duration, thumbnail, video_id = result

        song = Song(
            path=path,
            title=str(title),
            duration=str(duration),
            thumbnail=str(thumbnail),
            requester_id=ctx.author.id,
            video_id=str(video_id),
            time_started=int(time.time()),
        )

        if guild_id not in self.queues:
            self.queues[guild_id] = []

        if vc_chan and vc_chan.is_playing():
            self.queues[guild_id].append(song)
            embed = discord.Embed(
                title="Added to queue",
                description=f"**{title}** ({duration})",
                color=discord.Color.green(),
            )
            embed.set_image(url=thumbnail)
            await first_response.edit(embed=embed, content="")
            return

        user_vc_chan = ctx.author.voice.channel
        if not vc_chan:
            await user_vc_chan.connect()
            vc_chan = ctx.guild.voice_client
        else:
            await vc_chan.move_to(user_vc_chan)

        try:
            if not vc_chan or not isinstance(vc_chan, discord.VoiceClient):
                await first_response.edit(content="Voice client not connected.")
                return
            ffmpeg_options = {"executable": "ffmpeg.exe"} if sys.platform == "win32" else {}
            music = discord.FFmpegPCMAudio(path, **ffmpeg_options)
            self.current_song[guild_id] = song
            vc_chan.play(
                music,
                after=lambda _: self.bot.loop.call_soon_threadsafe(
                    lambda: asyncio.create_task(self._play_next(guild_id, ctx)),
                ),
            )
        except discord.DiscordException, OSError:
            logger.exception("Failed to play audio")
            self.current_song[guild_id] = None
            await first_response.edit(content="Failed to play audio.")
            return

        embed = discord.Embed(
            title="Started playing",
            description=f"**{title}** ({duration})",
            color=discord.Color.green(),
        )
        embed.set_image(url=thumbnail)
        await first_response.edit(embed=embed, content="")

    @commands.guild_only()
    @admin_check()
    @music.command(name="leave", description="Leaves a voice channel (Admin only).")
    async def leave(self, ctx: commands.Context) -> None:
        """Leaves the current voice channel."""
        if not ctx.guild.voice_client:
            await ctx.send("I'm not in a voice channel.", ephemeral=True)
            return

        guild_id = ctx.guild.id
        if guild_id in self.queues:
            self.queues[guild_id] = []
        self.current_song[guild_id] = None

        try:
            await ctx.guild.voice_client.disconnect()
        except discord.Forbidden, discord.HTTPException:
            await ctx.send("Failed to leave the voice channel.", ephemeral=True)
            return
        await ctx.send("Left the voice channel.")

    @commands.guild_only()
    @music.command(name="queue", description="Shows the current music queue")
    async def queue(self, ctx: commands.Context) -> None:
        """Shows the current music queue."""
        guild_id = ctx.guild.id
        queue = self.queues.get(guild_id, [])

        if not queue:
            await ctx.send("The queue is empty.")
            return

        queue_list = "\n".join(
            [
                f"**{i + 1}. {s.title}** ({s.duration}) - requested by <@{s.requester_id}>"
                for i, s in enumerate(queue)
            ],
        )

        embed = discord.Embed(
            title="Music Queue",
            description=queue_list,
            color=discord.Color.blue(),
        )
        embed.set_footer(
            text="Tip: use /music nowplaying to show currently playing song.",
        )
        await ctx.send(embed=embed)

    @admin_check()
    @commands.guild_only()
    @music.command(name="skip", description="Skips the currently playing song")
    async def skip(self, ctx: commands.Context) -> None:
        """Skips the currently playing song."""
        if not ctx.guild:
            return
        vc_chan = ctx.guild.voice_client
        if not vc_chan or not isinstance(vc_chan, discord.VoiceClient) or not vc_chan.is_playing():
            await ctx.send("Nothing is playing right now.")
            return

        vc_chan.stop()
        await ctx.send("Skipped the current song.")

    @commands.guild_only()
    @music.command(
        name="nowplaying",
        aliases=["np", "current"],
        description="Shows the currently playing song",
    )
    async def nowplaying(self, ctx: commands.Context) -> None:
        """Shows the currently playing song."""
        guild_id = ctx.guild.id
        song = self.current_song.get(guild_id)

        if not song or not ctx.guild.voice_client or not ctx.guild.voice_client.is_playing():
            await ctx.send("Nothing is playing right now.")
            return

        yt_url = f"https://www.youtube.com/watch?v={song.video_id}"
        embed = discord.Embed(
            title="Now Playing",
            description=f"**[{song.title}]({yt_url})**",
            color=discord.Color.blue(),
        )
        currently_at = format_duration(int(time.time() - song.time_started))
        embed.add_field(name="Currently at", value=currently_at, inline=True)
        embed.add_field(name="Duration", value=song.duration, inline=True)
        embed.add_field(
            name="Requested by",
            value=f"<@{song.requester_id}>",
            inline=True,
        )
        if song.thumbnail:
            embed.set_thumbnail(url=song.thumbnail)

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    """Add Music cog to the bot."""
    await bot.add_cog(Music(bot))
