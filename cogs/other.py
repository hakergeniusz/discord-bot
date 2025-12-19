import discord
from discord.ext import commands
from discord import app_commands

class other(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='source', description='Source of the bot.')
    async def test(interaction: discord.Interaction):
        await interaction.response.send_message('This bot is open-source! You can find the source on https://github.com/hakergeniusz/discord-bot')

async def setup(bot):
    await bot.add_cog(other(bot))
