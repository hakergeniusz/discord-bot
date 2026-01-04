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

import fastf1
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os
from core.config import status_map, does_exist, find_circuit, TMP_BASE, change_file, cowsay, CURRENT_YEAR

F1_DRIVER_is_used = 0

fastf1.Cache.enable_cache(os.path.join(TMP_BASE, 'fastf1'))

beeping = 0

class F1Commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name='f1_result', description='Outputs the result of an F1 race')
    @app_commands.describe(season="Season of the race you want the result of", roundnumber="Round number of the race asked. You can get one with /f1_calendar")
    async def f1_result(self, ctx: commands.Context, season: commands.Range[int, 1950, CURRENT_YEAR], roundnumber: commands.Range[int, 1, 24]): # Remember to change if F1 introduces an F1 calendar with more than 24 rounds.
        """Gives the result of an F1 race asked for."""
        await ctx.defer()

        global status_map
        if_existed = await does_exist(season, roundnumber)

        if not if_existed:
            await ctx.send(f"There wasn't R{roundnumber} in {season}.")
            return

        session = await asyncio.to_thread(fastf1.get_session, season, roundnumber, 'R')
        await asyncio.to_thread(session.load, telemetry=False, weather=False)

        results = session.results
        results1 = results.head(1000)

        is_there_data = 0
        result = []

        for _, row in results1.iterrows():
            pos = int(row['Position'])
            driver = row['FullName']
            team = row['TeamName']
            status = row['Status']
            label = status_map.get(status, status)

            if status == "Finished":
                result.append(f"{pos}. {driver} ({team})")
            else:
                if label:
                    result.append(f"{pos}. {driver} ({team}) - {label}")
                else:
                    result.append(f"{pos}. {driver} ({team})")

            is_there_data = 1

        if is_there_data == 0:
            response = await ctx.send(f'''There wasn't R{roundnumber} in {season} yet. Please check it after the race.''')
            await asyncio.sleep(3)
            if not ctx.interaction:
                await ctx.message.delete()
            await response.delete()
            return
        circuit = await find_circuit(season, roundnumber)
        output = "\n".join(result)

        if not ctx.interaction:
            message = f"""
**F1 {season} {circuit}:**
{output}
            """
            await ctx.send(message)
            return
        responseF1 = discord.Embed(
            title=f"F1 {season} {circuit}",
            description=output,
            color=discord.Color.red()
        )
        await ctx.send(embed=responseF1)

    @commands.hybrid_command(name="f1_calendar", description="Shows an F1 calendar")
    @app_commands.describe(season="Season of the calendar you want to know")
    async def f1_calendar(self, ctx: commands.Context, season: commands.Range[int, 1950, CURRENT_YEAR]):
        await ctx.defer()
        schedule = await asyncio.to_thread(fastf1.get_event_schedule, season)

        lines = []

        for _, row in schedule.iterrows():
            location = row['EventName']
            roundnumber = row['RoundNumber']
            sprint = row['EventFormat'] in ['sprint', 'sprint_shootout', 'sprint_qualifying']
            date = row['EventDate'].date()
            if sprint:
                lines.append(f'{roundnumber}. {location} (Sprint) - {date}')
            elif roundnumber == 0:
                lines.append(f'{location} - {date}')
            elif location == 'Pre-Season Testing':
                lines.append(f'{location} - {date}')
            else:
                lines.append(f'{roundnumber}. {location} - {date}')

        output = "\n".join(lines)
        if not ctx.interaction:
            message = f"""
**F1 {season} calendar:**
{output}
            """
            await ctx.send(message)
            return

        F1Calendar = discord.Embed(
            title=f"F1 {season} calendar",
            description=output,
            color=discord.Color.red()
        )
        await ctx.send(embed=F1Calendar)

    @commands.hybrid_command(name="f1_driver", description="Shows F1 driver's results in a season.")
    @app_commands.describe(driver_code="The 3-letter driver code (e.g. VER)", season="Season of the results you want to know.", show_not_started="Toggle for showing races with DNS (Default: False).")
    async def f1_driver(self, ctx: commands.Context, driver_code: commands.Range[str, 3, 3], season: commands.Range[int, 1950, CURRENT_YEAR], show_not_started: bool = False):
        """Gives the result of an F1 driver in a season."""
        global F1_DRIVER_is_used
        await ctx.defer()

        if driver_code.isalpha() != True:
            await ctx.send('Invalid driver code.')
            return

        if F1_DRIVER_is_used != 0:
            warning_message = await ctx.send(f'''Someone else is already using this command. Please wait until this message is replaced.
                                                    > Q: Why do I need to wait?
                                                    > A: This command when used by many people at once does not function correctly.''')
            while F1_DRIVER_is_used != 0:
                await asyncio.sleep(0.5)
            await warning_message.edit(content="It's your turn. Please wait a moment until I download the required data.")
        F1_DRIVER_is_used = 1
        driver_code = driver_code.upper()
        schedule = await asyncio.to_thread(fastf1.get_event_schedule, season)
        races = schedule[schedule['EventFormat'] != 'testing']
        results_list = []
        did_driver_race = 0
        for _, race in races.iterrows():
            round_num = race['RoundNumber']
            race_name = race['EventName']

            try:
                session = await asyncio.to_thread(fastf1.get_session, season, round_num, 'R')
                await asyncio.to_thread(session.load, laps=False, telemetry=False, weather=False, messages=False)
                driver_result = session.results[session.results['Abbreviation'] == driver_code]
                if not driver_result.empty:
                    pos = int(driver_result['Position'].iloc[0])
                    points = driver_result['Points'].iloc[0]
                    results_list.append(f"R{round_num}: **P{pos}** at {race_name} ({points} pts)")
                    did_driver_race += 1
                else:
                    if show_not_started:
                        results_list.append(f"R{round_num}: {race_name} - No Data/DNS")
            except Exception:
                continue

        if did_driver_race == 0:
            F1_DRIVER_is_used = 0
            response_to_user = await ctx.send(f"Could not find any results for driver {driver_code.upper()} in {season} season.")
            await asyncio.sleep(3)
            await ctx.message.delete()
            await response_to_user.delete()
            if warning_message:
                await warning_message.delete()
            return

        output = "\n".join(results_list)
        if not ctx.interaction:
            message = f"""
**F1 Season Results: {driver_code} ({season}):**
{output}
            """
            await ctx.send(message)
            F1_DRIVER_is_used = 0
            return
        F1Driver = discord.Embed(
            title=f"F1 Season Results: {driver_code} ({season})",
            description=output,
            color=discord.Color.red()
        )
        await ctx.send(embed=F1Driver)
        F1_DRIVER_is_used = 0
        if warning_message:
            await warning_message.delete()


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
    await bot.add_cog(F1Commands(bot))
    await bot.add_cog(Meme(bot))