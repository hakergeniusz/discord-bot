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
import asyncio
import os
import aiohttp
import random
from core.config import image_checker, process_prompt, create_file


class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="webhook", description="Sends a message to a Discord webhook")
    @app_commands.describe(webhook="URL of the webhook", message="Message that you want to send from the webhook", name="The name how webhook will appear", avatar_url="The avatar URL for the webhook")
    async def webhook(self, interaction: discord.Interaction, webhook: str, message: str, name: str = None, avatar_url: str = None):
        await interaction.response.defer()
        if not webhook.startswith(('https://discord.com/api/webhooks/', 'http://discord.com/api/webhooks/', 'discord.com/api/webhooks/')):
            await interaction.followup.send('Invalid webhook URL.', ephemeral=True)
            return
        if webhook.startswith('http://'):
            webhook = webhook.replace("http://", "https://", 1)
        elif webhook.startswith('discord.com'):
            webhook = webhook.replace("discord.com", "https://discord.com", 1)
        async with aiohttp.ClientSession() as session:
            async with session.get(webhook) as response:
                if response.status == 401:
                    await interaction.followup.send("Invalid webhook URL.", ephemeral=True)
                    print(f"{interaction.user.name} tried to send a message '{message}' to a webhook '{webhook}' but received status code 401.")
                    return

            if avatar_url:
                does_it_exist = await image_checker(session=session, image_link=avatar_url)
                if not does_it_exist:
                    await interaction.followup.send("Incorrect avatar URL.", ephemeral=True)
                    print(f"{interaction.user.name} thought that {avatar_url} was a URL...")
                    return

            data = {
                "content": message,
                "username": name,
                "avatar_url": avatar_url
            }

            async with session.post(webhook, json=data) as response:
                if response.status == 429:
                    await interaction.followup.send("Rate-limit has been hit. Message hasn't been sent.", ephemeral=True)
                    print(f"Failed to send a message to '{webhook}' of contents '{message}' because of rate limits")

                if response.status == 204:
                    await interaction.followup.send("Message sent successfully.", ephemeral=True)
                    print(f"Sent '{message}' to webhook '{webhook}'")

    @app_commands.command(name="say", description="Send a message to a channel")
    @app_commands.describe(
        message="Message to send",
        delete_after="How many seconds after sending should it be deleted.",
    )
    @app_commands.guild_only()
    async def say(self, interaction: discord.Interaction, message: str, delete_after: int = None):
        channel = await self.bot.fetch_channel(interaction.channel_id)
        wiadomosc = await channel.send(message)

        print(f"""On "{channel.name}" sent message: "{message}". User: {interaction.user.name}. """)
        await interaction.response.send_message(f"Message sent to <#{interaction.channel_id}>", ephemeral=True)

        if delete_after:
            await asyncio.sleep(delete_after)
            await wiadomosc.delete()
            await interaction.edit_original_response(content=f"Message sent to <#{interaction.channel_id}>, was removed due to request to remove it after {delete_after} seconds.")
            print(f"Removed '{message}' because of removal delay of {delete_after} seconds")

    @commands.hybrid_command(name="dm_or_not", description="Checks is the message sent in the DM or a server")
    async def dmornot(self, ctx: commands.Context):
        if ctx.guild:
            await ctx.send("It is a server")
        else:
            await ctx.send("It is a DM")

    @app_commands.command(name="ai", description="AI that will (maybe) respond to your questions.")
    @app_commands.describe(prompt="Message to the AI")
    async def ai(self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        print(f'{interaction.user.name} says: {prompt}')
        full_response = ""
        counter_ai = 0
        message = await interaction.followup.send('▌')
        async for chunk in process_prompt(prompt):
            full_response += chunk
            counter_ai += 1

            if len(full_response) <= 1900:
                if counter_ai % 10 == 0:
                    await message.edit(content=full_response + '▌')
            else:
                if len(full_response) <= 1912:
                    await message.edit(content='Response is too long to send it on Discord. Soon, file with full response will be provided.')

        if len(full_response) <= 1900:
            await message.edit(content=full_response)
            return

        file_name = os.path.join("tmp", f"{random.randint(100000, 999999)}.txt")
        await create_file(file_name=file_name, file_content=full_response)
        await asyncio.sleep(0.05)

        if not os.path.exists(file_name):
            await message.edit(content='Response is too long to send it on Discord. Error while making a file with full response.')
            return

        await message.delete()
        file = discord.File(f'{file_name}')
        await interaction.followup.send(content='Here is the file with the full response:', file=file)

        if os.path.exists(file_name):
            os.remove(file_name)

    @commands.guild_only()
    @commands.hybrid_command(name="hide_conversation", description="Hides the conversation")
    async def hide(self, ctx: commands.Context):
        """Tries to hide the conversation by sending many empty lines."""
        mes = '''

        '''
        mes = mes * 100
        mes = 'e' + mes + 'e'
        await ctx.send(mes)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Sends info when a message has been sent."""
        print(f'{message.author.name} said: {message.content}')


async def setup(bot):
    await bot.add_cog(Utility(bot))
