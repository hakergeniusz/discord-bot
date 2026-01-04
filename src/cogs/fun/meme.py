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
import asyncio
from core.config import TMP_BASE, change_file, cowsay

beeping = 0

class howmanybuttonButtons(discord.ui.View):
    """A class for ```/howmanybutton``` to work."""
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.success)
    async def howmanybutton_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        count = await asyncio.to_thread(change_file, os.path.join(TMP_BASE, 'howmanybutton'), interaction.user.id)
        if count == 1:
            content = f'<@{interaction.user.id}> clicked the button {count} time!'
        else:
            content = f'<@{interaction.user.id}> clicked the button {count} times!'
        await interaction.response.edit_message(content=content)


class Meme(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="beep", description="Beeps in the computer that is hosting the bot.")
    @app_commands.describe(
        times="How many times to beep (if not provided, default value is: 1)",
        beep_delay="Delay between beeps (in seconds, must be bigger than 0.05 and smaller than 5)"
    )
    async def beep(self, interaction: discord.Interaction, times: app_commands.Range[int, 2, 100] = 1, beep_delay: app_commands.Range[float, 0.05, 5.0] = None):
        """Beeps in the computer hosting the bot. If PC doesn't have a beeper, *beep* will give an error that no speaker found."""
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

    @commands.hybrid_command(name="nothing", description=".")
    async def nothing(self, ctx: commands.Context):
        """Literally nothing."""
        await ctx.send(f".", ephemeral=True)
        print(f"{ctx.author.name} tried nothing...")

    @commands.hybrid_command(name="howmanytimes", description="Says how many times was the command typed")
    async def howmanytimes(self, ctx: commands.Context):
        """Says how many times this user typed this command."""
        count = await asyncio.to_thread(change_file, os.path.join(TMP_BASE, 'howmanytimes'), ctx.author.id)

        if count == 1:
            await ctx.send(f'You have used this command {count} time.')
            return
        await ctx.send(f'You have used this command {count} times.')

    @commands.hybrid_command(name="complain", description="Compain to the bot owner.")
    async def complain(self, ctx: commands.Context):
        """Complaining to yourself why you wanted to complain to the bot owner."""
        await ctx.send('https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713', ephemeral=True)
        print(f"{ctx.author.name} complained and regretted it.")

    @commands.hybrid_command(name="heart", description="Shows a heart.")
    async def heart(self, ctx: commands.Context):
        await ctx.send(':middle_finger:', ephemeral=True)

    @commands.hybrid_command(name="finger", description="Shows a finger.")
    async def finger(self, ctx: commands.Context):
        await ctx.send(':heart:', ephemeral=True)

    @commands.hybrid_command(name="rickroll_me")
    async def rickroll(self, ctx: commands.Context):
        await ctx.send("Ok, if you want to be rickrolled, you will be.")
        await ctx.send('https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713')

    @app_commands.command(name="howmanybutton", description="How many times did you press the button?")
    async def howmanybutton(self, interaction: discord.Interaction):
        """Sends a message and says how many times the user clicked the button globally."""
        view = howmanybuttonButtons(interaction.client)
        await interaction.response.send_message('Click this button!', view=view)

    @commands.hybrid_command(name="cowsay", description="I'm a cow!")
    @app_commands.describe(text="What you want me to say?")
    async def cowsay(self, ctx: commands.Context, *, text: str):
        await ctx.send(cowsay(text))

async def setup(bot):
    await bot.add_cog(Meme(bot))
