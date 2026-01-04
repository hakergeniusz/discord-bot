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


class other(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", description="Pong! Outputs the latency of the bot.")
    async def ping(self, ctx: commands.Context):
        latency = round(self.bot.latency * 1000)
        await ctx.reply(f'Pong! Latency is {latency}ms')

    @commands.hybrid_command(name='source', description='Source of the bot.')
    async def source(self, ctx: commands.Context):
        if not ctx.interaction:
            await ctx.send('This bot is open-source! You can find the source here: https://github.com/hakergeniusz/discord-bot')
            return
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="View Source Code", url="https://github.com/hakergeniusz/discord-bot"))
        await ctx.send('This bot is open-source! You can find the source by clicking the following button:', view=view)

    @commands.hybrid_command(name='license', description="Bot's license information.")
    async def licence(self, ctx: commands.Context):
        if not ctx.interaction:
            message = """
            📜 **Legal Information & License**

**Copyright (C) 2026 hakergeniusz**
This program is free software: you can redistribute it and/or modify it under the terms of the **GNU General Public License v3.0** as published by the Free Software Foundation.

⚠️ Disclaimer of Warranty
This program is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of **MERCHANTABILITY** or **FITNESS FOR A PARTICULAR PURPOSE**. See the [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.txt) for more details.
            """
            await ctx.send(message)
            return
        embed = discord.Embed(
            title="📜 Legal Information & License",
            color=discord.Color.blue(),
            description=(
                "**Copyright (C) 2026 hakergeniusz**\n\n"
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
        await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(other(bot))
