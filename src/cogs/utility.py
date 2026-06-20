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

"""Module for utility commands including webhooks, say, and AI."""

import asyncio
import secrets
from pathlib import Path

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from core.ai import process_prompt
from core.config import (
    AI_RESPONSE_LIMIT,
    RATE_LIMIT_RESPONSE_CODE,
    SUCCESS_RESPONSE_CODE,
    TMP_BASE,
    UNAUTHORIZED_RESPONSE_CODE,
)
from core.howmany import create_file
from core.image_checker import image_checker


class Utility(commands.Cog):
    """Cog for utility commands like webhooks, say, and AI."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the Utility cog."""
        self.bot = bot

    @app_commands.command(
        name="webhook",
        description="Sends a message to a Discord webhook",
    )
    @app_commands.describe(
        webhook="URL of the webhook",
        message="Message that you want to send from the webhook",
        name="The name how webhook will appear",
        avatar_url="The avatar URL for the webhook",
    )
    @app_commands.checks.cooldown(1, 1.5, key=lambda i: (i.guild_id, i.user.id))
    async def webhook(
        self,
        interaction: discord.Interaction,
        webhook: str,
        message: str,
        name: str | None = None,
        avatar_url: str | None = None,
    ) -> None:
        """Sends a message to a Discord webhook."""
        await interaction.response.defer(ephemeral=True)
        if not webhook.startswith(
            (
                "https://discord.com/api/webhooks/",
                "http://discord.com/api/webhooks/",
                "discord.com/api/webhooks/",
            ),
        ):
            await interaction.followup.send("Invalid webhook URL.", ephemeral=True)
            return
        if webhook.startswith("http://"):
            webhook = webhook.replace("http://", "https://", 1)
        elif webhook.startswith("discord.com"):
            webhook = webhook.replace("discord.com", "https://discord.com", 1)
        async with aiohttp.ClientSession() as session:
            async with session.get(webhook) as response:
                if response.status == UNAUTHORIZED_RESPONSE_CODE:
                    await interaction.followup.send(
                        "Invalid webhook URL.",
                        ephemeral=True,
                    )
                    return

            if avatar_url:
                does_it_exist = await image_checker(
                    session=session,
                    image_link=avatar_url,
                )
                if does_it_exist is False:
                    await interaction.followup.send(
                        "Incorrect avatar URL.",
                        ephemeral=True,
                    )
                    return

            data = {"content": message, "username": name, "avatar_url": avatar_url}

            async with session.post(webhook, json=data) as response:
                if response.status == RATE_LIMIT_RESPONSE_CODE:
                    await interaction.followup.send(
                        "Rate-limit has been hit. ",
                        ephemeral=True,
                    )

                if response.status == SUCCESS_RESPONSE_CODE:
                    await interaction.followup.send(
                        "Message sent successfully.",
                        ephemeral=True,
                    )

    @app_commands.command(name="say", description="Send a message to a channel")
    @app_commands.describe(
        message="Message to send",
        delete_after="How many seconds after sending should it be deleted.",
    )
    @app_commands.guild_only()
    async def say(
        self,
        interaction: discord.Interaction,
        message: str,
        delete_after: int | None = None,
    ) -> None:
        """Send a message to a channel."""
        channel = await self.bot.fetch_channel(interaction.channel_id)
        msg = await channel.send(message)

        await interaction.response.send_message(
            f"Message sent to <#{interaction.channel_id}>",
            ephemeral=True,
        )

        if delete_after:
            await asyncio.sleep(delete_after)
            await msg.delete()
            msg_text = (
                f"Message sent to <#{interaction.channel_id}>, was removed due "
                f"to request to remove it after {delete_after} seconds."
            )
            await interaction.edit_original_response(content=msg_text)

    @commands.hybrid_command(
        name="dm_or_not",
        description="Checks is the message sent in the DM or a server",
    )
    async def dmornot(self, ctx: commands.Context) -> None:
        """Checks if the command was triggered in a DM or a server."""
        if ctx.guild:
            await ctx.send("It is a server")
        else:
            await ctx.send("It is a DM")

    @commands.hybrid_command(
        name="ai",
        description="AI that will (maybe) respond to your questions.",
    )
    @app_commands.describe(prompt="Message to the AI")
    @commands.cooldown(1, 15, commands.BucketType.member)
    async def ai(self, ctx: commands.Context, *, prompt: str) -> None:
        """AI that responds to user questions using Gemma 4 31B."""
        await ctx.defer()
        full_response = ""
        counter_ai = 0
        message = await ctx.send("▌")
        async for chunk in process_prompt(prompt):
            full_response += chunk
            counter_ai += 1

            if len(full_response) <= AI_RESPONSE_LIMIT:
                if counter_ai % 10 == 0:
                    await message.edit(content=full_response + "▌")
            elif len(full_response) <= AI_RESPONSE_LIMIT + 12:
                await message.edit(
                    content="Response is too long to send it on Discord. "
                    "Soon, file with full response will be provided.",
                )

        if len(full_response) <= AI_RESPONSE_LIMIT:
            await message.edit(content=full_response)
            return

        file_path = Path(TMP_BASE) / f"{secrets.randbelow(900000) + 100000}.txt"
        await create_file(file_name=str(file_path), file_content=full_response)
        await asyncio.sleep(0.05)

        if not file_path.exists():
            await message.edit(
                content="Response is too long to send it on Discord. "
                "Error while making a file with full response.",
            )
            return

        await message.delete()
        file = discord.File(str(file_path))
        await ctx.send(content="Here is the file with the full response:", file=file)

        if file_path.exists():
            file_path.unlink()

    @commands.guild_only()
    @commands.hybrid_command(
        name="hide_conversation",
        description="Hides the conversation",
    )
    async def hide(self, ctx: commands.Context) -> None:
        """Hides the conversation by sending many empty lines."""
        mes = """

        """
        mes = mes * 100
        mes = "e" + mes + "e"
        await ctx.send(mes)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """Log messages to the console."""


async def setup(bot: commands.Bot) -> None:
    """Add Utility cog to the bot."""
    await bot.add_cog(Utility(bot))
