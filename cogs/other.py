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

    @app_commands.command(name="ping", description="Pong! Outputs the latency of the bot.")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f'Pong! Latency is {latency}ms')

    @app_commands.command(name='source', description='Source of the bot.')
    async def source(self, interaction: discord.Interaction):
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="View Source Code", url="https://github.com/hakergeniusz/discord-bot"))
        await interaction.response.send_message('This bot is open-source! You can find the source by clicking the following button:', view=view)

    @app_commands.command(name='licence', description="Bot's license information.")
    async def licence(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📜 Legal Information & License",
            color=discord.Color.blue(),
            description=(
                "**Copyright (C) 2025 hakergeniusz**\n\n"
                "This program is free software: you can redistribute it and/or modify "
                "it under the terms of the **GNU General Public License v3.0** as "
                "published by the Free Software Foundation.\n\n"
                "### ⚠️ Disclaimer of Warranty\n"
                "This program is distributed in the hope that it will be useful, "
                "but **WITHOUT ANY WARRANTY**; without even the implied warranty of "
                "**MERCHANTABILITY** or **FITNESS FOR A PARTICULAR PURPOSE**. "
                "See the [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.txt) for more details."
            )
        )
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="View Source Code", url="https://github.com/hakergeniusz/discord-bot"))
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(other(bot))
