import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os

load_dotenv()
owner_id = int(os.environ.get('OWNER_ID'))

def admin_check():
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.user.id == owner_id:
            return True
        await interaction.response.send_message("You don't have required permissions to do that.", ephemeral=True)
        return False
    return app_commands.check(predicate)

class StatusButtons(discord.ui.View):
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
    @app_commands.command(name="shutdown", description="[OWNER ONLY] Turns off the bot", )
    async def shutdown(self, interaction: discord.Interaction):
        await interaction.response.send_message("Shutting down the bot...", ephemeral=True)
        print("Shutting down the bot")
        await self.bot.close()
        # Why not this?
        crash = 10 / 0

    @admin_check()
    @app_commands.command(name="purge", description="Removes messages in a chat.", )
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.describe(
        range="How many messages you want to delete (max: 100)"
    )
    @app_commands.guild_only()
    async def purge(self, interaction: discord.Interaction, range: app_commands.Range[int, 1, 100]):
        bot_perms = interaction.app_permissions.manage_messages
        if not bot_perms:
            await interaction.response.send_message("I don't have necessary permissions to do that.")
            return
        chan = interaction.channel
        if range == 1:
            await interaction.response.send_message(f"Deleting {range} message...", ephemeral=True)
        else:
            await interaction.response.send_message(f"Deleting {range} messages...", ephemeral=True)
        await chan.purge(limit=range)
        if range == 1:
            await interaction.edit_original_response(content=f'Deleted {range} message successfully.')
            print(f"Deleted {range} message in {interaction.channel.name}")
        else:
            await interaction.edit_original_response(content=f'Deleted {range} messages successfully.')
            print(f"Deleted {range} messages in {interaction.channel.name}")

    @admin_check()
    @app_commands.command(name="change_status", description="Changes the status of the bot")
    async def change_status(self, interaction: discord.Interaction):
        view = StatusButtons(interaction.client)
        await interaction.response.send_message("Select the status:", view=view, ephemeral=True)

    @admin_check()
    @app_commands.command(name="pc_turn_off", description="Turns off the PC")
    async def pc_turn_off(self, interaction: discord.Interaction):
        os.system('poweroff')

    @admin_check()
    @app_commands.command(name='create_webhook', description='Creates a webhook.')
    @app_commands.guild_only()
    async def create_webhook(self, interaction: discord.Interaction):
        webhook = await interaction.channel.create_webhook(name="Test webhook")
        await interaction.response.send_message(f'{webhook.url}', ephemeral=True)

    @admin_check()
    @app_commands.command(name='delete_webhook', description='Deletes a webhook')
    @app_commands.describe(webhook='Webhook link.')
    async def delete_webhook(self, interaction: discord.Interaction, webhook: str):
        res = requests.delete(webhook)
        if res == 404 or res == 401:
            await interaction.response.send_message('This webhook does not exist. You may have already deleted it.')
        elif res == 200 or res == 204:
            await interaction.response.send_message('Removed webhook successfully')
        else:
            await interaction.response.send_message(f'Webhook may not have been deleted. Response code is {res}.')

async def setup(bot):
    await bot.add_cog(ownerCommands(bot))
