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
import asyncio
from ollama import AsyncClient
import os
import aiohttp

OWNER_ID = int(os.environ['DISCORD_OWNER_ID'])
HASTEBIN_API_KEY = os.environ['HASTEBIN_API_KEY']

SYSTEM_PROMPT = """
You are a chatbot for a Discord command (don't mention this in responses).
Don't include any unnecessary text in your responses and don't use emojis unless explicitly asked.
You are free to make reponses that are longer than 2000 characters or any higher count.
"""

async def safety_filter(message):
    message = {
        'role': 'user',
        'content': message
    }
    response_safety = await AsyncClient().chat(model='llama-guard3:1b', messages=[message])
    response_safety = response_safety['message']['content']
    if response_safety == 'safe':
        return True
    else:
        return None

async def process_prompt(message, model):
    response = await AsyncClient().chat(
        model=model,
        messages=[{'role': 'system', 'content': SYSTEM_PROMPT}, {'role': 'user', 'content': message}],
        stream=True
    )
    async for chunk in response:
        content = chunk['message']['content']
        yield content

IMAGE_CONTENT_TYPES = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
    'image/svg+xml'
]

async def image_checker(session: aiohttp.ClientSession, image_link: str):
    if not image_link:
        return True
    try:
        async with session.head(image_link, timeout=3) as response:
            if response.status != 200:
                return None
            content_type = response.headers.get('Content-Type', '').lower()
            for image_type in IMAGE_CONTENT_TYPES:
                if content_type.startswith(image_type):
                    return True
            return None
    except Exception:
        return None

class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="webhook", description="Sends a message to a webhook")
    @app_commands.describe(webhook="URL of the webhook", message="Message that you want to send from the webhook", name="The name how webhook will appear", avatar_url="The avatar URL for the webhook")
    async def webhook(self, interaction: discord.Interaction, webhook: str, message: str, name: str = None, avatar_url: str = None):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get(webhook) as response:
                if response.status == 401:
                    await interaction.followup.send("Invalid webhook URL.", ephemeral=True)
                    print(f"{interaction.user.name} tried to send a message '{message}' to a webhook '{webhook}' but 401")
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
        reason="Reason why you want to send it", # lol
        delete_after="How many seconds after sending should it be deleted.",
    )
    async def say(self, interaction: discord.Interaction, message: str, reason: str = None, delete_after: int = None):
        channel = await self.bot.fetch_channel(interaction.channel_id)
        wiadomosc = await channel.send(message)
        if interaction.guild:
            print(f"""On "{channel.name}" sent message: "{message}". User: {interaction.user.name}. """)
        else:
            print(f"""On DM sent message: "{message}". User: {interaction.user.name}. """)
        if reason:
            print(f"""Reason: "{reason}". """)
        await interaction.response.send_message(f"Message sent to <#{interaction.channel_id}>", ephemeral=True)
        if delete_after:
            await asyncio.sleep(delete_after)
            await wiadomosc.delete()
            await interaction.edit_original_response(content=f"Message sent to <#{interaction.channel_id}>, was removed due to request to remove it after {delete_after} seconds.")
            print(f"Removed '{message}' because of removal delay of {delete_after} seconds")

    @app_commands.command(name="dm_or_not", description="Checks is the message sent in the DM or a channel")
    async def dmornot(self, interaction: discord.Interaction):
        if interaction.guild:
            await interaction.response.send_message("It is a server", ephemeral=True)
            print(f"{interaction.user.name} checked is it a DM or a guild and it is a guild")
        else:
            await interaction.response.send_message("It is a DM", ephemeral=True)
            print(f"{interaction.user.name} checked is it a DM or a guild and it is a DM")

    @app_commands.command(name="ai", description="AI that will (maybe) respond to your questions.")
    @app_commands.describe(prompt="Message to the AI")
    @app_commands.choices(model=[
        app_commands.Choice(name="gemma3:1b", value="gemma3:1b"),
        app_commands.Choice(name="gemma3:4b", value="gemma3:4b"), # this line
        app_commands.Choice(name="qwen2.5-coder:7b", value="qwen2.5-coder:7b"), # and this line
    ])
    async def ai(self, interaction: discord.Interaction, prompt: str, model: app_commands.Choice[str]):
        await interaction.response.defer()
        print(f'{interaction.user.name} says: {prompt}')
        print(f'Using model: {model.value}')
        message = await interaction.followup.send('Loading model...')
        full_response = ""
        counter_ai = 0
        async for chunk in process_prompt(prompt, model.value):
            full_response += chunk
            counter_ai += 1
            if len(full_response) <= 1900:
                if counter_ai % 10 == 0:
                    await message.edit(content=full_response + '▌')
            else:
                await message.edit(content='Response is too long to send it on Discord. Soon link for hastebin will be provided.')
                break
        if len(full_response) <= 1900:
            await message.edit(content=full_response)
            return
        headers = {
            "Authorization": f"Bearer {HASTEBIN_API_KEY}",
            "Content-Type": "text/plain"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post("https://hastebin.com/documents", data=full_response, headers=headers) as response:
                if response.status != 200:
                    await message.edit(content=f'Failed to upload to Hastebin: Status code: {response.status}.')
                    return
                if not 'key' in data:
                    await message.edit(content='Failed to upload to Hastebin: not recieved the link with response.')
                    return
                data = await response.json()
                await message.edit(content=f'Response is too long to send it on Discord. You can see the response here: <{f"https://hastebin.com/share/{data['key']}"}>.')

    @app_commands.command(name="ping", description="Pong! Outputs the latency of the bot.")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f'Pong! Latency is {latency}ms')

    @app_commands.command(name="test", description="Reserved for testing purposes.")
    @app_commands.guild_only()
    async def test(self, interaction: discord.Interaction):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message('You are not permitted to do that.')
            return
        await interaction.response.defer()
        server = interaction.guild
        chan = await server.create_text_channel('test')
        mes = await interaction.followup.send(f'<#{chan.id}>')
        tasks = []
        for _ in range(5):
            tasks.append(chan.send(f'<@{interaction.user.id}>'))
        await asyncio.gather(*tasks, return_exceptions=True)
        await asyncio.sleep(3)
        await chan.delete()
        await mes.delete()

    @app_commands.command(name="hide", description="Hides the conversation")
    async def hide(self, interaction: discord.Interaction):
        mes = '''

        '''
        for _ in range(6):
            mes += mes
        mes = 'e' + mes + 'e'
        await interaction.response.send_message(mes)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        print(f'{message.author.name} said: {message.content}')

async def setup(bot):
    await bot.add_cog(Utility(bot))