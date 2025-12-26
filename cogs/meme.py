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
import os
import asyncio

beeping = 0

def create_file_howmanytimes(id: int):
    """Creates a file for change_file()."""
    if not id:
        return

    path = 'tmp/howmanytimes/'

    if os.path.exists(f'{path}{id}.txt'):
        return

    with open(f'{path}{id}.txt','w') as f:
        f.write('0')


def change_file_howmanytimes(id: int):
    """Made for /howmanytimes to work. Adds 1 to a file and returns the new number and returns the new count."""
    path = 'tmp/howmanytimes/'

    if not os.path.exists(f'{path}{id}.txt'):
        create_file_howmanytimes(id)

    with open(f'{path}{id}.txt', 'r') as f:
        count = int(f.read())

    with open(f'{path}{id}.txt', 'w') as f:
        f.write(f'{count + 1}')
        return count + 1


class Meme(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="beep", description="Beeps in the computer that is hosting the bot.")
    @app_commands.describe(
        times="How many times to beep (if not provided, default value is: 1)",
        beep_delay="Delay between beeps (in seconds, must be bigger than 0.05 and smaller than 5)"
    )
    async def beep(self, interaction: discord.Interaction, times: app_commands.Range[int, 2, 100] = 1, beep_delay: app_commands.Range[float, 0.05, 5.0] = None):
        """Beeps in the computer hosting the bot. If you don't have a beeper, *beep* will give an error that no speaker found."""
        global beeping
        if beeping == 1:
            await interaction.response.send_message(f"<@{interaction.user.id}>, you cannot beep while I am already beeping. Please try again later.")
            print(f"An idiot named {interaction.user.name} wanted to beep when I already beeped")
            return

        beeping = 1
        if times == 1:
            await interaction.response.send_message(f"<@{interaction.user.id}>, I will beep {times} time in the computer.")
            print(f"An idiot named {interaction.user.name} wants to beep once.")
            process = await asyncio.create_subprocess_shell('beep')
            await process.communicate()
            beeping = 0
            return

        if beep_delay:
            if beep_delay < 1 or beep_delay > 1:
                await interaction.response.send_message(f"<@{interaction.user.id}>, I will beep {times} times with the delay between of them of {beep_delay} seconds in the computer.")
            else:
                await interaction.response.send_message(f"<@{interaction.user.id}>, I will beep {times} times with the delay between of them of {beep_delay} second in the computer.")
        else:
            await interaction.response.send_message(f"<@{interaction.user.id}>, I will beep {times} times in the computer.")
        print(f"An idiot named {interaction.user.name} wants to beep {times} times with {beep_delay} second of delay between them.")

        for i in range(times):
            process = await asyncio.create_subprocess_shell('beep')
            await process.communicate()
            if beep_delay:
                await asyncio.sleep(beep_delay)
        beeping = 0

    @app_commands.command(name="nothing", description=".")
    async def nothing(self, interaction: discord.Interaction):
        """Literally nothing."""
        await interaction.response.send_message(f".", ephemeral=True)
        print(f"{interaction.user.name} tried nothing...")

    @app_commands.command(name="howmanytimes", description="Says how many times was the command typed")
    async def howmanytimes(self, interaction: discord.Interaction):
        """Says how many times this user typed this command."""
        count = await asyncio.to_thread(change_file_howmanytimes, interaction.user.id)

        if count == 1:
            await interaction.response.send_message(f'You have used this command {count} time.')
            return
        await interaction.response.send_message(f'You have used this command {count} times.')

    @app_commands.command(name="complain", description="Compain to the bot owner.")
    async def complain(self, interaction: discord.Interaction):
        """Complaining to yourself why you wanted to complain to the bot owner."""
        await interaction.response.send_message('https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713', ephemeral=True)
        print(f"{interaction.user.name} complained and regretted it.")

    @app_commands.command(name="heart", description="Shows a heart.")
    async def heart(self, interaction: discord.Interaction):
        """Shows a middle finger emoji."""
        await interaction.response.send_message(':middle_finger:', ephemeral=True)

    @app_commands.command(name="finger", description="Shows a finger.")
    async def finger(self, interaction: discord.Interaction):
        """Shows a heart emoji."""
        await interaction.response.send_message(':heart:', ephemeral=True)

    @app_commands.command(name="rickroll_me")
    async def rickroll(self, interaction: discord.Interaction):
        """Rickrolls the user that typed this command."""
        await interaction.response.send_message('Not this time.')
        await asyncio.sleep(3)

        await interaction.followup.send('But maybe?')
        await asyncio.sleep(3)

        await interaction.followup.send('https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713')


async def setup(bot):
    await bot.add_cog(Meme(bot))
