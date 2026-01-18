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
import asyncio
import os
from core.config import TMP_BASE,CURRENT_YEAR
from core.cowsay import cowsay
from core.f1 import race_result, f1_season_calendar, f1_standings_py
from core.howmany import change_file

class F1Commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='f1_race_result', description='Outputs the result of an F1 race')
    @app_commands.describe(
        season="Season of the race you want the result of",
        roundnumber="Round number of the race asked. You can get one with /f1_calendar",
        emojis='Default is True, if False, emojis for podium positions will not be given.'
    )
    async def f1_race_result(self, ctx: commands.Context, season: commands.Range[int, 1950, CURRENT_YEAR], roundnumber: commands.Range[int, 1, 24], emojis: bool = True): # Remember to change if F1 introduces an F1 calendar with more than 24 rounds.
        """Gives the result of an F1 race asked for."""
        await ctx.defer()
        grand_prix_name, results_list = await race_result(season=season, roundnumber=roundnumber, emojis=emojis)
        if grand_prix_name is None or results_list == []:
            await ctx.send(f'Could not find R{roundnumber} in {season} F1 season.')
            return
        results = "\n".join(results_list)
        responseF1 = discord.Embed(
            title=f"F1 {grand_prix_name} ({season})",
            description=results,
            color=discord.Color.red()
        )
        await ctx.send(embed=responseF1)

    @commands.hybrid_command(name="f1_calendar", description="Shows an F1 calendar")
    @app_commands.describe(season="Season of the calendar you want to know")
    async def f1_calendar(self, ctx: commands.Context, season: commands.Range[int, 1950, CURRENT_YEAR]):
        await ctx.defer()
        calendar_list = await f1_season_calendar(season)
        if calendar_list == []:
            await ctx.send(f'No calendar found for {season}.')
            return
        calendar = "\n".join(calendar_list)
        if not ctx.interaction:
            message = f"""
**F1 {season} calendar:**
{calendar}
            """
            await ctx.send(message)
            return

        F1Calendar = discord.Embed(
            title=f"F1 {season} calendar",
            description=calendar,
            color=discord.Color.red()
        )
        await ctx.send(embed=F1Calendar)

    @commands.hybrid_command(name="f1_standings", description="Shows F1 standings for a season.")
    @app_commands.describe(season="Season you want standings for.")
    async def f1_standings(self, ctx: commands.Context, season: commands.Range[int, 1950, CURRENT_YEAR]):
        await ctx.defer()
        standings_list = await f1_standings_py(season)
        if standings_list == []:
            await ctx.send(f'No standings found for {season}.')
            return
        standings = "\n".join(standings_list)
        if not ctx.interaction:
            message = f"**F1 {season} standings:**\n{standings}"
            await ctx.send(message)
            return

        F1Standings = discord.Embed(
            title=f"F1 {season} standings",
            description=standings,
            color=discord.Color.red()
        )
        await ctx.send(embed=F1Standings)


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

    @commands.hybrid_command(name="nothing", description=".")
    async def nothing(self, ctx: commands.Context):
        """Literally nothing."""
        await ctx.send(".", ephemeral=True)
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

    @commands.hybrid_command(name="rickroll_me", description="Rickrolls the user.")
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
    async def cowsay(self, ctx: commands.Context, *, text: str = None):
        if text and len(text) >= 250:
            await ctx.send("You can't say that much!")
            return
        await ctx.send(cowsay(text))

async def setup(bot):
    await bot.add_cog(F1Commands(bot))
    await bot.add_cog(Meme(bot))