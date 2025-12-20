#  Copyright (C) 2025 hakergeniusz
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

class other(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='source', description='Source of the bot.')
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message('This bot is open-source! You can find the source on https://github.com/hakergeniusz/discord-bot')

async def setup(bot):
    await bot.add_cog(other(bot))
