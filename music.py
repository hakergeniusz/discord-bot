import discord
from discord.ext import commands
from discord import app_commands

def is_it_vc(interaction):
    voice_channels = interaction.guild.voice_channels
    for vc in voice_channels:
            if vc.id == interaction.channel_id:
                return True
    return None

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="play", description="Plays music on a voice channel")
    @app_commands.describe(channel1="Channel to play music on")
    @app_commands.guild_only()
    async def play(self, interaction: discord.Interaction, channel1: discord.VoiceChannel):
        if not interaction.user.voice:
            await interaction.response.send_message("You are not in a voice channel.")
            print(f"{interaction.user.name} tried to rupture his eardrums, but he isn't in a VC, so I can't do it.")
            return
        vc_chan = interaction.guild.voice_client
        if not vc_chan:
            await channel1.connect()
            print(f'Joined {channel1.name} to rupture eardrums of {interaction.user.name}')
            vc_chan = interaction.guild.voice_client
        else:
            await vc_chan.move_to(channel1)
        if vc_chan.is_playing():
            await interaction.response.send_message("Already playing audio.")
            print(f"{interaction.user.name} tried to rupture his eardrums, but I already do it. ")
            return
        music = discord.FFmpegPCMAudio('what.mp3')
        vc_chan.play(music)
        await interaction.response.send_message(f"Playing audio on <#{channel1.id}>")
        print(f"Rupturing the eardrums of {interaction.user.name}")


    @app_commands.command(name="join_vc", description="Joins a voice channel")
    @app_commands.guild_only()
    async def join_vc(self, interaction: discord.Interaction):
        if not interaction.user.voice:
            await interaction.response.send_message(f"You are not in a voice channel.", ephemeral=True)
            return

        if not is_it_vc(interaction):
            await interaction.response.send_message('Type this in a voice channel.')
            return
        channel = interaction.channel
        await channel.connect()
        await interaction.response.send_message(f"Joined <#{interaction.channel_id}>", ephemeral=True)
        print(f"Joined {interaction.channel.name} with {interaction.user.name}")

    @app_commands.command(name="leave_vc", description="Leaves a voice channel.")
    @app_commands.guild_only()
    async def leave(self, interaction: discord.Interaction):
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
            await interaction.response.send_message("Left the voice channel.")
            print(f"Leaving {interaction.channel.name} due to request of {interaction.user.name}")
        else:
            await interaction.response.send_message("I'm not in a voice channel.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Music(bot))
