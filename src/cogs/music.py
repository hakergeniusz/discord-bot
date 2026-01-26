# Copyright (C) 2026 hakergeniusz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from core.admin_check import admin_check
from core.youtube import download_youtube_video


@app_commands.guild_only()
@commands.guild_only()
class Music(commands.Cog):
    """Cog for playing music from YouTube."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the Music cog."""
        self.bot = bot
        self.queues = {}

    def _play_next(self, guild_id: int, interaction: discord.Interaction) -> None:
        """Plays the next song in the queue for a guild."""
        if guild_id not in self.queues or not self.queues[guild_id]:
            return

        vc_chan = interaction.guild.voice_client
        if not vc_chan:
            return

        path, title, duration = self.queues[guild_id].pop(0)
        try:
            music = discord.FFmpegPCMAudio(path)
            vc_chan.play(
                music,
                after=lambda e: self._play_next(guild_id, interaction),
            )
            asyncio.run_coroutine_threadsafe(
                interaction.channel.send(f"Now playing: **{title}**"), self.bot.loop
            )
        except Exception as e:
            print(f"Error playing next song: {e}")
            self._play_next(guild_id, interaction)

    @commands.hybrid_group(name="music", invoke_without_command=True)
    async def music(self, ctx: commands.Context) -> None:
        """Default command used to group other ones."""
        if ctx.invoked_subcommand is None:
            await ctx.send("Available commands: play, skip, leave, queue.")

    @music.command(name="play", description="Plays music on a voice channel")
    @app_commands.describe(youtube_url="Youtube URL of the video you want to play.")
    async def play(
        self,
        ctx: commands.Context,
        youtube_url: str = "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    ) -> None:
        """Plays music from a YouTube URL in a voice channel."""
        await ctx.defer()
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("You are not in a voice channel.")
            return

        vc_chan = ctx.guild.voice_client
        guild_id = ctx.guild.id

        first_response = await ctx.send(
            "Attempting to download the video. This may take a while..."
        )
        path, title, duration = await asyncio.to_thread(
            download_youtube_video, youtube_url
        )
        if path is None:
            await first_response.edit(content="Incorrect URL/Failed to download video.")
            return

        if guild_id not in self.queues:
            self.queues[guild_id] = []

        if vc_chan and vc_chan.is_playing():
            self.queues[guild_id].append((path, title, duration))
            await first_response.edit(
                content=f"Added to queue: **{title}** ({duration})"
            )
            return

        user_vc_chan = ctx.author.voice.channel
        if not vc_chan:
            await user_vc_chan.connect()
            vc_chan = ctx.guild.voice_client
        else:
            await vc_chan.move_to(user_vc_chan)

        try:
            music = discord.FFmpegPCMAudio(path)
            vc_chan.play(
                music,
                after=lambda e: self._play_next(guild_id, ctx),
            )
        except Exception:
            await first_response.edit(content="Failed to play audio.")
            return

        await first_response.edit(content=f"Playing audio on <#{user_vc_chan.id}>")
        print(f"Rupturing the eardrums of {ctx.author.name}")

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

        try:
            await ctx.guild.voice_client.disconnect()
        except (discord.Forbidden, discord.HTTPException):
            await ctx.send("Failed to leave the voice channel.", ephemeral=True)
            return
        await ctx.send("Left the voice channel.")
        print(f"Leaving {ctx.channel.name} due to request of {ctx.author.name}")

    @music.command(name="queue", description="Shows the current music queue")
    async def queue(self, ctx: commands.Context) -> None:
        """Shows the current music queue."""
        guild_id = ctx.guild.id
        if guild_id not in self.queues or not self.queues[guild_id]:
            await ctx.send("The queue is empty.")
            return

        queue_list = "\n".join(
            [
                f"{i + 1}. **{title}** ({duration})"
                for i, (_, title, duration) in enumerate(self.queues[guild_id])
            ]
        )
        await ctx.send(f"Current queue:\n{queue_list}")

    @admin_check()
    @music.command(name="skip", description="Skips the currently playing song")
    async def skip(self, ctx: commands.Context) -> None:
        """Skips the currently playing song."""
        vc_chan = ctx.guild.voice_client
        if not vc_chan or not vc_chan.is_playing():
            await ctx.send("Nothing is playing right now.")
            return

        vc_chan.stop()
        await ctx.send("Skipped the current song.")


async def setup(bot: commands.Bot) -> None:
    """Add Music cog to the bot."""
    await bot.add_cog(Music(bot))
