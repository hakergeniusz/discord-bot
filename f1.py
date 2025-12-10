import fastf1
from fastf1 import get_session, events
import discord
from discord.ext import commands
from discord import app_commands
import datetime
import asyncio

CURRENT_YEAR = datetime.date.today().year

fastf1.Cache.enable_cache('/home/hakergeniusz/Dokumenty/Python/discord/tmp/f1_cache')

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
        return 'nyjfdhyhutgfjbnfbhurttghj'


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
        session.load(telemetry=False, weather=False)
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


async def setup(bot):
    await bot.add_cog(F1Commands(bot))