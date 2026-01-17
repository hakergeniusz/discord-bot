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
from discord import app_commands
import os
import aiohttp
from core.config import PC_POWEROFF
from core.admin_check import admin_check, admin_check_slash
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
        print("Shutting down the bot...")
        await self.bot.close()

    @admin_check()
    @commands.hybrid_command(name="purge", description="Removes messages in a chat.", )
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(range="How many messages you want to delete (max: 100)")
    @commands.guild_only()
    async def purge(self, ctx: commands.Context, range: commands.Range[int, 1, 100]):
        if ctx.interaction:
            await ctx.defer(ephemeral=True)
        bot_perms = ctx.permissions.manage_messages
        if not bot_perms:
            await ctx.send("I don't have necessary permissions to do that.")
            return

        chan = ctx.channel
        if ctx.message:
            try:
                await ctx.message.delete()
            except (discord.Forbidden, discord.HTTPException):
                pass
        await chan.purge(limit=range)

        text_reply = f'Deleted {range} messages successfully.'
        if ctx.interaction:
            message = await ctx.reply(text_reply)
            return
        message = await ctx.send(text_reply)

        await asyncio.sleep(3)
        try:
            await message.delete()
        except Exception:
            pass

    @admin_check_slash()
    @app_commands.command(name="change_status", description="Changes the status of the bot")
    async def change_status(self, interaction: discord.Interaction):
        view = StatusButtons(interaction.client)
        await interaction.response.send_message("Select the status:", view=view, ephemeral=True)

    @admin_check()
    @commands.hybrid_command(name="turn_off_pc", description="Turns off the PC")
    async def pc_turn_off(self, ctx: commands.Context):
        """Turns off the computer hosting the bot."""
        if not PC_POWEROFF:
            await ctx.send("PC cannot be turned off, because I have not been allowed to do so.")
            return
        os.system('poweroff')

    @admin_check()
    @commands.hybrid_command(name='create_webhook', description='Creates a webhook.')
    @commands.guild_only()
    async def create_webhook(self, ctx: commands.Context):
        """Creates a webhook for the current channel."""
        try:
            webhook = await ctx.channel.create_webhook(name="Test webhook")
            await ctx.send(f'{webhook.url}', ephemeral=True)
        except discord.Forbidden:
            await ctx.send("I am forbidden to create a webhook in this channel (I don't have permissions).")
        except Exception:
            await ctx.send("Failed to create webhook.")

    @admin_check()
    @commands.hybrid_command(name='delete_webhook', description='Deletes a webhook')
    @app_commands.describe(webhook='Webhook link.')
    async def delete_webhook(self, ctx: commands.Context, webhook: str):
        async with aiohttp.ClientSession() as session:
            async with session.delete(webhook) as response:
                if response.status in (401, 404):
                    await ctx.send('This webhook does not exist. You may have already deleted it.')
                elif response.status in (200, 204):
                    await ctx.send('Removed webhook successfully')
                else:
                    await ctx.send(f'Webhook may not have been deleted. Response code is {response.status}.')


async def setup(bot):
    await bot.add_cog(ownerCommands(bot))
