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
import os
import aiohttp
from core.config import admin_check, PC_POWEROFF
import asyncio

class StatusButtons(discord.ui.View):
    """A cog for /change_status to work."""
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @discord.ui.button(label="Online", style=discord.ButtonStyle.success)
    async def online_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.bot.change_presence(status=discord.Status.online)
        await interaction.response.send_message("Status set to Online", ephemeral=True)
        print("Status set to Online")

    @discord.ui.button(label="Do Not Disturb", style=discord.ButtonStyle.danger)
    async def dnd_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.bot.change_presence(status=discord.Status.dnd)
        await interaction.response.send_message("Status set to Do Not Disturb", ephemeral=True)
        print("Status set to Do Not Disturb")

    @discord.ui.button(label="Idle", style=discord.ButtonStyle.secondary)
    async def idle_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.bot.change_presence(status=discord.Status.idle)
        await interaction.response.send_message("Status set to Idle", ephemeral=True)
        print("Status set to Idle")

    @discord.ui.button(label="Invisible (offline)", style=discord.ButtonStyle.primary)
    async def invisible_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.bot.change_presence(status=discord.Status.invisible)
        await interaction.response.send_message("Status set to Invisible", ephemeral=True)
        print("Status set to Invisible")


class ownerCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @admin_check()
    @commands.hybrid_command(name="shutdown", description="[OWNER ONLY] Turns off the bot", )
    async def shutdown(self, ctx: commands.Context):
        await ctx.send("Shutting down the bot...")
        print("Shutting down the bot")
        await self.bot.close()

    @admin_check()
    @commands.hybrid_command(name="purge", description="Removes messages in a chat.", )
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(range="How many messages you want to delete (max: 100)")
    @commands.guild_only()
    async def purge(self, ctx: commands.Context, range: commands.Range[int, 1, 100]):
        bot_perms = ctx.permissions.manage_messages
        if not bot_perms:
            await ctx.send("I don't have necessary permissions to do that.")
            return

        chan = ctx.channel
        if range == 1:
            await ctx.send(f"Deleting {range} message...")
        else:
            await ctx.send(f"Deleting {range} messages...")

        await chan.purge(limit=2)
        await chan.purge(limit=range)

        if range == 1:
            message = await ctx.send(content=f'Deleted {range} message successfully.')
            print(f"Deleted {range} message in {ctx.channel.name}")
        else:
            message = await ctx.send(content=f'Deleted {range} messages successfully.')
            print(f"Deleted {range} messages in {ctx.channel.name}")
        await asyncio.sleep(3)
        await ctx.message.delete()
        await message.delete()

    @admin_check()
    @app_commands.command(name="change_status", description="Changes the status of the bot")
    async def change_status(self, interaction: discord.Interaction):
        view = StatusButtons(interaction.client)
        await interaction.response.send_message("Select the status:", view=view, ephemeral=True)

    @admin_check()
    @app_commands.command(name="turn_off_pc", description="Turns off the PC")
    async def pc_turn_off(self, interaction: discord.Interaction):
        """Turns off the computer hosting the bot."""
        if not PC_POWEROFF:
            await interaction.response.send_message("PC cannot be turned off, because I have not been permitted from doing so.")
            return
        os.system('poweroff')

    @admin_check()
    @app_commands.command(name='create_webhook', description='Creates a webhook.')
    @app_commands.guild_only()
    async def create_webhook(self, interaction: discord.Interaction):
        """Creates a webhook for the current channel."""
        webhook = await interaction.channel.create_webhook(name="Test webhook")
        await interaction.response.send_message(f'{webhook.url}', ephemeral=True)

    @admin_check()
    @app_commands.command(name='delete_webhook', description='Deletes a webhook')
    @app_commands.describe(webhook='Webhook link.')
    async def delete_webhook(self, interaction: discord.Interaction, webhook: str):
        async with aiohttp.ClientSession() as session:
            async with session.delete(webhook) as response:
                if response.status in (401, 404):
                    await interaction.response.send_message('This webhook does not exist. You may have already deleted it.')
                elif response.status in (200, 204):
                    await interaction.response.send_message('Removed webhook successfully')
                else:
                    await interaction.response.send_message(f'Webhook may not have been deleted. Response code is {response.status}.')

    @admin_check()
    @commands.hybrid_command(name='send_messages')
    @app_commands.describe(count="how many messages")
    async def send_messages(self, ctx: commands.Context, count: commands.Range[int, 1, 100]):
        for i in range(count):
            await ctx.send(f'{i + 1}')


async def setup(bot):
    await bot.add_cog(ownerCommands(bot))
