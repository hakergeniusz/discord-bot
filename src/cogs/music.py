#  Copyright (C) 2026 hakergeniusz
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import discord
from discord.ext import commands
from discord import app_commands
from core.config import PROJECT_ROOT, download_youtube_video
import os

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="play", description="Plays music on a voice channel")
    @app_commands.describe(youtube_url="Youtube URL of the video you want to play.")
    @app_commands.guild_only()
    async def play(self, interaction: discord.Interaction, youtube_url: str):
        await interaction.response.defer()
        if not interaction.user.voice:
            await interaction.followup.send("You are not in a voice channel.")
            print(f"{interaction.user.name} tried to rupture his eardrums, but he isn't in a VC, so I can't do it.")
            return
        vc_chan = interaction.guild.voice_client
        if vc_chan.is_playing():
                await interaction.followup.send("Already playing audio.")
                print(f"{interaction.user.name} tried to rupture his eardrums, but I already do it. ")
                return
        path = download_youtube_video(youtube_url)
        if not path:
            await interaction.followup.send("Incorrect URL/Failed to download video.")
            return
        user_vc_chan = interaction.user.voice.channel
        if not interaction.guild.voice_client:
            await user_vc_chan.connect()
            print(f'Joined {user_vc_chan.name} to rupture eardrums of {interaction.user.name}')
            vc_chan = interaction.guild.voice_client
        else:
            await vc_chan.move_to(user_vc_chan)

        music = discord.FFmpegPCMAudio(path)
        vc_chan.play(music)

        await interaction.followup.send(f"Playing audio on <#{user_vc_chan.id}>")
        print(f"Rupturing the eardrums of {interaction.user.name}")

    @commands.hybrid_command(name="join_vc", description="Joins a voice channel")
    @app_commands.guild_only()
    async def join_vc(self, ctx: commands.Context):
        """Joins a voice channel user is connected to."""
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("You are not in a voice channel.", ephemeral=True)
            return

        voice_channel = ctx.author.voice.channel
        if ctx.guild.voice_client:
            await ctx.guild.voice_client.connect(voice_channel)
        else:
            await voice_channel.connect()

        await ctx.send(f"Joined <#{voice_channel.id}>", ephemeral=True)
        print(f"Joined {voice_channel.name} with {ctx.author.name}")

    @commands.hybrid_command(name="leave_vc", description="Leaves a voice channel.")
    @commands.guild_only()
    async def leave(self, ctx: commands.Context):
        if not ctx.guild.voice_client:
            await ctx.send("I'm not in a voice channel.", ephemeral=True)
            return
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Left the voice channel.")
        print(f"Leaving {ctx.channel.name} due to request of {ctx.author.name}")


async def setup(bot):
    await bot.add_cog(Music(bot))
