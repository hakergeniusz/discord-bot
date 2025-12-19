import discord
from discord.ext import commands
from discord import app_commands

class ExampleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='test', description='Lorem ipsum dolor sit amet.')
    async def test(interaction: discord.Interaction):
        await interaction.response.send_message('Lorem ipsum dolor sit amet.')

async def setup(bot):
    await bot.add_cog(ExampleCog(bot))
