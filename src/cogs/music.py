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

import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from core.youtube import download_youtube_video
from core.admin_check import admin_check

@app_commands.guild_only()
class Music(commands.GroupCog, group_name="music"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="play", description="Plays music on a voice channel")
    @app_commands.describe(youtube_url="Youtube URL of the video you want to play.")
    @app_commands.guild_only()
    async def play(self, interaction: discord.Interaction, youtube_url: str):
        await interaction.response.defer()
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.followup.send("You are not in a voice channel.")
            return
        vc_chan = interaction.guild.voice_client
        if vc_chan and vc_chan.is_playing():
            await interaction.followup.send("Already playing audio.")
            return
        first_response = await interaction.followup.send('Attempting to download the video. This may take a while...')
        path = await asyncio.to_thread(download_youtube_video, youtube_url)
        if not path:
            await first_response.edit(content="Incorrect URL/Failed to download video.")
            return

        user_vc_chan = interaction.user.voice.channel
        if not vc_chan:
            await user_vc_chan.connect()
            vc_chan = interaction.guild.voice_client
        else:
            await vc_chan.move_to(user_vc_chan)

        try:
            music = discord.FFmpegPCMAudio(path)
            vc_chan.play(music)
        except Exception:
            await first_response.edit(content="Failed to play audio.")
            return

        await first_response.edit(content=f"Playing audio on <#{user_vc_chan.id}>")
        print(f"Rupturing the eardrums of {interaction.user.name}")

    @commands.hybrid_command(name="join", description="Joins a voice channel")
    @app_commands.guild_only()
    async def join_vc(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("You are not in a voice channel.", ephemeral=True)
            return

        voice_channel = ctx.author.voice.channel
        try:
            if ctx.guild.voice_client:
                await ctx.guild.voice_client.connect(voice_channel)
            else:
                await voice_channel.connect()
        except (discord.Forbidden, discord.HTTPException):
            await ctx.send("Could not join the voice channel.", ephemeral=True)
            return

        await ctx.send(f"Joined <#{voice_channel.id}>", ephemeral=True)
        print(f"Joined {voice_channel.name} with {ctx.author.name}")

    @admin_check()
    @commands.hybrid_command(name="leave", description="Leaves a voice channel (Admin only)")
    @commands.guild_only()
    async def leave(self, ctx: commands.Context):
        if not ctx.guild.voice_client:
            await ctx.send("I'm not in a voice channel.", ephemeral=True)
            return
        try:
            await ctx.guild.voice_client.disconnect()
        except (discord.Forbidden, discord.HTTPException):
            await ctx.send("Failed to leave the voice channel.", ephemeral=True)
            return
        await ctx.send("Left the voice channel.")
        print(f"Leaving {ctx.channel.name} due to request of {ctx.author.name}")


async def setup(bot):
    await bot.add_cog(Music(bot))
