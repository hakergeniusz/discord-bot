# Copyright (c) 2025-2026 hakergeniusz
#
# Licensed under the EUPL, Version 1.2 or - as soon they will be approved by the European
# Commission - subsequent versions of the EUPL (the "Licence"); You may not use this work
# except in compliance with the Licence.
#
# You may obtain a copy of the Licence at:
# https://joinup.ec.europa.eu/software/page/eupl
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the Licence for the specific language
# governing permissions and limitations under the Licence.

"""Module for administrative commands and bot status management."""

import asyncio
import contextlib

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from core.admin_check import admin_check, admin_check_slash
from core.logger import get_logger

# Module-level logger
logger = get_logger(__name__)


class StatusButtons(discord.ui.View):
    """View with buttons to change the bot's status."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the StatusButtons view."""
        super().__init__()
        self.bot = bot
        logger.debug("StatusButtons view created")

    @discord.ui.button(label="Online", style=discord.ButtonStyle.success)
    async def online_button(
        self,
        interaction: discord.Interaction,
        _button: discord.ui.Button,
    ) -> None:
        """Set the bot's status to Online."""
        await self.bot.change_presence(status=discord.Status.online)
        await interaction.response.send_message("Status set to Online", ephemeral=True)
        logger.info("Bot status set to Online")

    @discord.ui.button(label="Do Not Disturb", style=discord.ButtonStyle.danger)
    async def dnd_button(
        self,
        interaction: discord.Interaction,
        _button: discord.ui.Button,
    ) -> None:
        """Set the bot's status to Do Not Disturb."""
        await self.bot.change_presence(status=discord.Status.dnd)
        await interaction.response.send_message(
            "Status set to Do Not Disturb",
            ephemeral=True,
        )
        logger.info("Bot status set to Do Not Disturb")

    @discord.ui.button(label="Idle", style=discord.ButtonStyle.secondary)
    async def idle_button(
        self,
        interaction: discord.Interaction,
        _button: discord.ui.Button,
    ) -> None:
        """Set the bot's status to Idle."""
        await self.bot.change_presence(status=discord.Status.idle)
        await interaction.response.send_message("Status set to Idle", ephemeral=True)
        logger.info("Bot status set to Idle")

    @discord.ui.button(label="Invisible (offline)", style=discord.ButtonStyle.primary)
    async def invisible_button(
        self,
        interaction: discord.Interaction,
        _button: discord.ui.Button,
    ) -> None:
        """Set the bot's status to Invisible."""
        await self.bot.change_presence(status=discord.Status.invisible)
        await interaction.response.send_message(
            "Status set to Invisible",
            ephemeral=True,
        )
        logger.info("Bot status set to Invisible")


class AdminCommands(commands.Cog):
    """Cog for commands restricted to the admins."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the AdminCommands cog."""
        self.bot = bot
        logger.debug("AdminCommands cog initialized")

    @admin_check()
    @commands.hybrid_command(
        name="shutdown",
        description="[ADMIN ONLY] Turns off the bot",
    )
    async def shutdown(self, ctx: commands.Context) -> None:
        """Turns off the bot. Restricted to admins."""
        logger.info("Shutdown command invoked by %s", ctx.author)
        await ctx.send("Shutting down the bot...")
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
        self,
        ctx: commands.Context,
        range_val: commands.Range[int, 1, 100],
    ) -> None:
        """Removes messages in a chat.

        Maximum of 100 messages, due to Discord API limit.
        """
        logger.info("Purge command invoked by %s for %d messages", ctx.author, range_val)
        if ctx.interaction:
            await ctx.defer(ephemeral=True)
        bot_perms = ctx.permissions.manage_messages
        if not bot_perms:
            await ctx.send("I don't have necessary permissions to do that.")
            logger.warning("Purge aborted: missing manage_messages permission")
            return

        chan = ctx.channel
        if ctx.message:
            with contextlib.suppress(discord.Forbidden, discord.HTTPException):
                await ctx.message.delete()
        await chan.purge(limit=range_val)

        text_reply = f"Deleted {range_val} messages successfully."
        if ctx.interaction:
            message = await ctx.reply(text_reply)
            logger.info("Purge succeeded, message sent via interaction")
            return
        message = await ctx.send(text_reply)
        logger.info("Purge succeeded, message sent")

        await asyncio.sleep(3)
        with contextlib.suppress(discord.Forbidden, discord.HTTPException):
            await message.delete()
            logger.debug("Purge reply message deleted")

    @admin_check_slash()
    @app_commands.command(
        name="change_status",
        description="Changes the status of the bot",
    )
    async def change_status(self, interaction: discord.Interaction) -> None:
        """Sends a message with buttons to change the status of the bot."""
        logger.info("Change status command invoked by %s", interaction.user)
        view = StatusButtons(interaction.client)
        await interaction.response.send_message(
            "Select the status:",
            view=view,
            ephemeral=True,
        )

    @admin_check()
    @commands.hybrid_command(name="create_webhook", description="Creates a webhook.")
    @commands.guild_only()
    async def create_webhook(self, ctx: commands.Context) -> None:
        """Creates a webhook for the current channel."""
        logger.info("Create webhook command invoked by %s", ctx.author)
        try:
            webhook = await ctx.channel.create_webhook(name="Test webhook")
            await ctx.send(f"{webhook.url}", ephemeral=True)
            logger.info("Webhook created at %s", webhook.url)
        except discord.Forbidden:
            await ctx.send(
                "I am forbidden to create a webhook in this channel (I don't have permissions).",
            )
            logger.warning("Webhook creation forbidden")
        except discord.HTTPException, aiohttp.ClientError:  # works in python 3.14!
            await ctx.send("Failed to create webhook.")
            logger.exception("Webhook creation failed")

    @commands.hybrid_command(name="delete_webhook", description="Deletes a webhook")
    @app_commands.describe(webhook="Webhook link.")
    async def delete_webhook(self, ctx: commands.Context, webhook: str) -> None:
        """Deletes a webhook from the a channel."""
        logger.info("Delete webhook command invoked by %s", ctx.author)
        async with (
            aiohttp.ClientSession() as session,
            session.delete(webhook) as response,
        ):
            if response.status in (401, 404):
                await ctx.send(
                    "This webhook does not exist. You may have already deleted it.",
                )
                logger.warning("Webhook deletion failed: not found")
            elif response.status in (200, 204):
                await ctx.send("Removed webhook successfully")
                logger.info("Webhook removed successfully")
            else:
                await ctx.send(
                    f"Webhook may not have been deleted. Response code is {response.status}.",
                )
                logger.warning("Webhook deletion returned status %s", response.status)


async def setup(bot: commands.Bot) -> None:
    """Add AdminCommands cog to the bot."""
    logger.debug("Setting up AdminCommands cog")
    await bot.add_cog(AdminCommands(bot))
