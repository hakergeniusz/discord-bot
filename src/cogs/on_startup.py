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
import os
import asyncio

class SyncCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        os.system('clear')
        print("-" * 40)
        print(f'Logged on as "{self.bot.user}"')
        print("-" * 40)
        print("Copyright (C) 2026 hakergeniusz")
        print("This program comes with ABSOLUTELY NO WARRANTY.")
        print("This is free software under the GNU AGPLv3.")
        print("-" * 40)
        await self.bot.tree.sync()
        await asyncio.sleep(2)
        await self.bot.change_presence(activity=None, status=discord.Status.dnd)


async def setup(bot):
    await bot.add_cog(SyncCog(bot))
