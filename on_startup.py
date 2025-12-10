import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
owner_id = int(os.environ.get('owner_id'))

class SyncCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged on as "{self.bot.user}"')
        await self.bot.tree.sync()
        await asyncio.sleep(2)
        await self.bot.change_presence(activity=None, status=discord.Status.dnd)
        #await asyncio.sleep(3)
        #await self.bot.change_presence(activity=None, status=discord.Status.dnd)

class OwnerNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # It is irritating so I removed it.
    #@commands.Cog.listener()
    #async def on_ready(self):
    #    latency = round(self.bot.latency * 1000)
    #    owner = await self.bot.fetch_user(owner_id)
    #    owner_dm = await owner.create_dm()
    #    await owner_dm.send(f'<@{owner_id}> Hello! Bot has been started, current ping is {latency}ms. ', delete_after=5)

async def setup(bot):
    await bot.add_cog(SyncCog(bot))
    await bot.add_cog(OwnerNotifier(bot))