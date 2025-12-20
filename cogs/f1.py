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

import fastf1
from fastf1 import get_session, events
import discord
from discord.ext import commands
from discord import app_commands
import datetime
import asyncio

CURRENT_YEAR = datetime.date.today().year

fastf1.Cache.enable_cache('tmp/fastf1')

status_map = {
    "Lapped": "Lapped",
    "Retired": "DNF",
    "Accident": "DNF (Accident)",
    "Collision": "DNF (Collision)",
    "Spun off": "DNF (Spin)",
    "Not classified": "NC",
    "Gearbox": "DNF (Gearbox)",
    "Engine": "DNF (Engine)",
    "Transmission": "DNF (Transmission)",
    "Electrical": "DNF (Electrical)",
    "Out of fuel": "DNF (Fuel)",
    "Oil leak": "DNF (Oil)",
    "Brakes": "DNF (Brakes)",
    "Suspension": "DNF (Suspension)",
    "Tyre": "DNF (Tyre)",
    "Cooling": "DNF (Cooling)",
    "Did not start": "DNS",
    "Withdrew": "DNS",
    "Injury": "DNS",
    "Illness": "DNS",
    "Disqualified": "DSQ",
    "Oil pressure": "DNF (Oil)",
    "Clutch": "DNF (Clutch)",
    "Supercharger": "DNF (Supercharger)",
    "Hydraulics": "DNF (Hydraulics)"
}

async def find_circuit(season, roundnumber):
    schedule = await asyncio.to_thread(fastf1.get_event_schedule, season)
    row = schedule.loc[schedule['RoundNumber'] == roundnumber]

    if not row.empty:
        event_name = row.iloc[0]['EventName']
        return f"{event_name}"
    else:
        return None

async def did_exist(season, roundnumber):
    schedule = await asyncio.to_thread(fastf1.get_event_schedule, season)
    event_row = schedule.loc[schedule['RoundNumber'] == roundnumber]
    if event_row.empty:
        return None
    else:
        return True

class F1Commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='f1_result', description='Outputs the result of an F1 race')
    @app_commands.describe(season="Season of the race you want the result of", roundnumber="Round number of the race asked. You can get one with /f1_calendar")
    async def f1_result(self, interaction: discord.Interaction, season: app_commands.Range[int, 1950, CURRENT_YEAR], roundnumber: app_commands.Range[int, 1, 24]): # Remember to change if F1 introduces an F1 calendar with more than 24 rounds.
        await interaction.response.defer()
        global status_map
        if_existed = await did_exist(season, roundnumber)
        if not if_existed:
            await interaction.followup.send(f"There wasn't {roundnumber} round in {season}.")
            return
        session = await asyncio.to_thread(fastf1.get_session, season, roundnumber, 'R')
        await asyncio.to_thread(session.load, telemetry=False, weather=False)
        results = session.results
        results1 = results.head(1000)

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
        circuit = await find_circuit(season, roundnumber)
        output = "\n".join(result)
        responseF1 = discord.Embed(
            title=f"F1 {season} {circuit}",
            description=output,
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=responseF1)

    @app_commands.command(name="f1_calendar", description="Shows an F1 calendar")
    @app_commands.describe(season="Season of the calendar you want to know")
    async def f1_calendar(self, interaction: discord.Interaction, season: app_commands.Range[int, 1950, CURRENT_YEAR]):
        await interaction.response.defer(ephemeral=True)
        checking_f1_driver = 1
        schedule = await asyncio.to_thread(fastf1.get_event_schedule, season)
        lines = []
        for _, row in schedule.iterrows():
            location = row['EventName']
            roundnumber = row['RoundNumber']
            sprint = row['EventFormat']
            date = row['EventDate'].date()
            if sprint == 'sprint':
                lines.append(f'{roundnumber}. {location} (Sprint) - {date}')
            elif sprint == 'sprint_shootout':
                lines.append(f'{roundnumber}. {location} (Sprint) - {date}')
            elif sprint == 'sprint_qualifying':
                lines.append(f'{roundnumber}. {location} (Sprint) - {date}')
            elif roundnumber == 0:
                lines.append(f'{location} - {date}')
            else:
                lines.append(f'{roundnumber}. {location} - {date}')
        output = "\n".join(lines)
        F1Calendar = discord.Embed(
            title=f"F1 {season} calendar",
            description=output,
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=F1Calendar)

    # Many users at once using this may cause this command to malfunction. Fix this later.
    @app_commands.command(name="f1_driver", description="Shows F1 driver's results in a season.")
    @app_commands.describe(driver_code="The 3-letter driver code (e.g. VER)", season="Season of the results you want to know.")
    async def f1_driver(self, interaction: discord.Interaction, driver_code: str, season: app_commands.Range[int, 1950, CURRENT_YEAR]):
        await interaction.response.defer()
        driver_code = driver_code.upper()
        schedule = await asyncio.to_thread(fastf1.get_event_schedule, season)
        races = schedule[schedule['EventFormat'] != 'testing']
        results_list = []
        for _, race in races.iterrows():
            round_num = race['RoundNumber']
            race_name = race['EventName']
            try:
                session = await asyncio.to_thread(fastf1.get_session, season, round_num, 'R')
                await asyncio.to_thread(session.load, laps=False, telemetry=False, weather=False, messages=False)
                driver_result = session.results[session.results['Abbreviation'] == driver_code]
                if not driver_result.empty:
                    pos = int(driver_result['Position'].iloc[0])
                    status = driver_result['Status'].iloc[0]
                    points = driver_result['Points'].iloc[0]
                    results_list.append(f"R{round_num}: **P{pos}** at {race_name} ({points} pts)")
                else:
                    results_list.append(f"R{round_num}: {race_name} - No Data/DNS")
            except Exception:
                continue
        if not results_list:
            await interaction.followup.send(f"Could not find any results for driver '{driver_code}' in {season}.")
            return
        output = "\n".join(results_list)
        F1Driver = discord.Embed(
            title=f"F1 Season Results: {driver_code} ({season})",
            description=output,
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=F1Driver)

async def setup(bot):
    await bot.add_cog(F1Commands(bot))
