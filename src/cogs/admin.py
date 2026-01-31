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

"""Module for administrative commands and bot status management."""

import asyncio

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from core.admin_check import admin_check, admin_check_slash


class StatusButtons(discord.ui.View):
    """View with buttons to change the bot's status."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the StatusButtons view."""
        super().__init__()
        self.bot = bot

    @discord.ui.button(label="Online", style=discord.ButtonStyle.success)
    async def online_button(
        self, interaction: discord.Interaction, _button: discord.ui.Button
    ) -> None:
        """Set the bot's status to Online."""
        await self.bot.change_presence(status=discord.Status.online)
        await interaction.response.send_message("Status set to Online", ephemeral=True)
        print("Status set to Online")

    @discord.ui.button(label="Do Not Disturb", style=discord.ButtonStyle.danger)
    async def dnd_button(
        self, interaction: discord.Interaction, _button: discord.ui.Button
    ) -> None:
        """Set the bot's status to Do Not Disturb."""
        await self.bot.change_presence(status=discord.Status.dnd)
        await interaction.response.send_message(
            "Status set to Do Not Disturb", ephemeral=True
        )
        print("Status set to Do Not Disturb")

    @discord.ui.button(label="Idle", style=discord.ButtonStyle.secondary)
    async def idle_button(
        self, interaction: discord.Interaction, _button: discord.ui.Button
    ) -> None:
        """Set the bot's status to Idle."""
        await self.bot.change_presence(status=discord.Status.idle)
        await interaction.response.send_message("Status set to Idle", ephemeral=True)
        print("Status set to Idle")

    @discord.ui.button(label="Invisible (offline)", style=discord.ButtonStyle.primary)
    async def invisible_button(
        self, interaction: discord.Interaction, _button: discord.ui.Button
    ) -> None:
        """Set the bot's status to Invisible."""
        await self.bot.change_presence(status=discord.Status.invisible)
        await interaction.response.send_message(
            "Status set to Invisible", ephemeral=True
        )
        print("Status set to Invisible")


class OwnerCommands(commands.Cog):
    """Cog for commands restricted to the bot owner."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the OwnerCommands cog."""
        self.bot = bot

    @admin_check()
    @commands.hybrid_command(
        name="shutdown",
        description="[OWNER ONLY] Turns off the bot",
    )
    async def shutdown(self, ctx: commands.Context) -> None:
        """Turns off the bot. Restricted to owner."""
        await ctx.send("Shutting down the bot...")
        print("Shutting down the bot...")
        await self.bot.close()

    @admin_check()
    @commands.hybrid_command(
        name="purge",
        description="Removes messages in a chat.",
    )
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(range_val="How many messages you want to delete (max: 100)")
    @commands.guild_only()
    async def purge(
        self, ctx: commands.Context, range_val: commands.Range[int, 1, 100]
    ) -> None:
        """Removes messages in a chat.

        Maximum of 100 messages, due to Discord API limit.
        """
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
        await chan.purge(limit=range_val)

        text_reply = f"Deleted {range_val} messages successfully."
        if ctx.interaction:
            message = await ctx.reply(text_reply)
            return
        message = await ctx.send(text_reply)

        await asyncio.sleep(3)
        try:
            await message.delete()
        except (discord.Forbidden, discord.HTTPException):
            pass

    @admin_check_slash()
    @app_commands.command(
        name="change_status", description="Changes the status of the bot"
    )
    async def change_status(self, interaction: discord.Interaction) -> None:
        """Sends a message with buttons to change the status of the bot."""
        view = StatusButtons(interaction.client)
        await interaction.response.send_message(
            "Select the status:", view=view, ephemeral=True
        )

    @admin_check()
    @commands.hybrid_command(name="create_webhook", description="Creates a webhook.")
    @commands.guild_only()
    async def create_webhook(self, ctx: commands.Context) -> None:
        """Creates a webhook for the current channel."""
        try:
            webhook = await ctx.channel.create_webhook(name="Test webhook")
            await ctx.send(f"{webhook.url}", ephemeral=True)
        except discord.Forbidden:
            await ctx.send(
                "I am forbidden to create a webhook in this channel "
                "(I don't have permissions)."
            )
        except (discord.HTTPException, aiohttp.ClientError):
            await ctx.send("Failed to create webhook.")

    @admin_check()
    @commands.hybrid_command(name="delete_webhook", description="Deletes a webhook")
    @app_commands.describe(webhook="Webhook link.")
    async def delete_webhook(self, ctx: commands.Context, webhook: str) -> None:
        """Deletes a webhook from the current channel."""
        async with aiohttp.ClientSession() as session:
            async with session.delete(webhook) as response:
                if response.status in (401, 404):
                    await ctx.send(
                        "This webhook does not exist. You may have already deleted it."
                    )
                elif response.status in (200, 204):
                    await ctx.send("Removed webhook successfully")
                else:
                    await ctx.send(
                        f"Webhook may not have been deleted. Response code "
                        f"is {response.status}."
                    )


async def setup(bot: commands.Bot) -> None:
    """Add OwnerCommands cog to the bot."""
    await bot.add_cog(OwnerCommands(bot))
