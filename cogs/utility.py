import discord
from discord.ext import commands
from discord import app_commands
import requests
import asyncio
from ollama import chat, ChatResponse
import os

owner_id = int(os.environ.get('OWNER_ID'))
def safety_filter(message):
    response_s: ChatResponse = chat(model='llama-guard3:1b', messages=[
        {
            'role': 'user',
            'content': message,
        },
    ])
    response_s = response_s['message']['content']
    if response_s == 'safe':
        return True
    else:
        return None

def ai(message):
    if not safety_filter(message):
        return False
    response: ChatResponse = chat(model='gemma3:270m', messages=[
        {
            'role': 'user',
            'content': message,
        },
    ])
    print(response)
    response = response['message']['content']
    idk = safety_filter(response)
    if not idk:
        return None
    return response

class CogListener(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        print(f'{message.author.name} said: {message.content}')

class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="webhook", description="Sends a message to a webhook")
    @app_commands.describe(webhook="URL of the webhook", message="Message that you want to send from the webhook", name="The name how webhook will appear", avatar_url="URL of the avatar you want to appear")
    async def webhook(self, interaction: discord.Interaction, webhook: str, message: str, name: str = None, avatar_url: str = None):
        attempt = requests.post(webhook)
        if attempt.status_code == 401:
            await interaction.response.send_message("Invalid webhook URL.", ephemeral=True)
            print(f"{interaction.user.name} tried to send a message '{message}' to a webhook '{webhook}' but 401")
        if avatar_url:
            av_test = requests.post(avatar_url)
            if av_test == 404:
                await interaction.response.send_message("Incorrect avatar URL", ephemeral=True)
                print(f"{interaction.user.name} thought that {avatar_url} was a URL ")
                avatar_url = None
        data = {
            "content": message,
            "username": name,
            "avatar_url": avatar_url
        }
        sent = requests.post(webhook, json = data)
        if sent.status_code == 429:
            await interaction.response.send_message("Rate-limit has been hit. Message hasn't been sent.", ephemeral=True)
            print(f"Failed to send a message to '{webhook}' of contents '{message}' because of rate limit")
        if sent.status_code == 204:
            await interaction.response.send_message("Message sent successfully.", ephemeral=True)
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
        if interaction.guild is None:
            await interaction.response.send_message("It is a DM", ephemeral=True)
            print(f"{interaction.user.name} checked is it a DM or a guild and it is a DM")
        if interaction.guild:
            await interaction.response.send_message("It is a server", ephemeral=True)
            print(f"{interaction.user.name} checked is it a DM or a guild and it is a guild")

    @app_commands.command(name="ai", description="gemma3:270m")
    @app_commands.describe(prompt="Message to the AI")
    async def ai (self, interaction: discord.Interaction, prompt: str):
        await interaction.response.defer()
        print(f'{interaction.user.name} says: {prompt}')
        response = ai(prompt)
        if response == None:
            await interaction.response.send_message('AI response did not pass safety systems. Please try again.')
            return
        elif response == False:
            await interaction.response.send_message('Your input did not pass safety systems. Please try again with a different one')
        else:
            if len(response) > 4000:
                print(f'{interaction.user.name} wanted a reply, but it was longer than 4000 characters. It was: {response}')
                await interaction.followup.send('Message was longer than 4000 characters, so it was not sent. Please try again.', ephemeral=True)
                return
            print(f'Reply to {interaction.user.name}')
            await interaction.followup.send(f'{response}', ephemeral=True)

    @app_commands.command(name="ping", description="Pong! Outputs the latency of the bot.")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f'Pong! Latency is {latency}ms')

    @app_commands.command(name="test", description="Reserved for testing purposes.")
    @app_commands.guild_only()
    async def test(self, interaction: discord.Interaction):
        if interaction.user.id != owner_id:
            await interaction.response.send_message('You are not permitted to do that.')
            return
        await interaction.response.defer()
        if not interaction.guild:
            await interaction.followup.send('Cannot do it in DMs', ephemeral=True)
            return
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
        if not message.guild:
            return
        ai_thingy = safety_filter(message.content)
        if not ai_thingy:
            await message.delete()
            return

async def setup(bot):
    await bot.add_cog(Utility(bot))
    await bot.add_cog(CogListener(bot))
