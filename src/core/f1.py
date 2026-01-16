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

import aiohttp
from core.config import status_map, CURRENT_YEAR


async def race_result(season: int, roundnumber: int, emojis: bool = True) -> list:
    """Gives the result of an F1 race session using Jolpica API.

    Args:
        season (int)
        roundnumber (int): Race number in F1 calendar to check.
        emojis (bool): Default is True, if False, emojis for first three positions will not be given.

    Returns:
        str: Circuit's name.
        list: A list with session results.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.jolpi.ca/ergast/f1/{season}/{roundnumber}/results/') as response:
            if response.status in range(400, 499):
                return None, []

            response = await response.json()
            response = response['MRData']['RaceTable']['Races']
            if response == []:
                return None, []
            circuit_name = response[0]['raceName']
            results = []
            for result in response[0]['Results']:
                POS = result['position']
                if emojis:
                    if POS == '1':
                        POS = '🥇'
                    elif POS == '2':
                        POS = '🥈'
                    elif POS == '3':
                        POS = '🥉'
                    else:
                        POS = f'{POS}.'
                else:
                    POS = f'{POS}.'
                DriverName = result['Driver']['givenName'] + ' ' + result['Driver']['familyName']
                TEAM = result['Constructor']['name']
                status = result['status']
                status = status_map.get(status, status)
                if status == 'Finished':
                    results.append(f'{POS} {DriverName} ({TEAM})')
                else:
                    results.append(f'{POS} {DriverName} ({TEAM}) - {status}')

            return circuit_name, results


async def f1_season_calendar(season: int) -> list:
    """Gives the F1 calendar using Jolpica API.

    Args:
        season (int): Season to find the calendar for.

    Returns:
        list: A list with all races in the season.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.jolpi.ca/ergast/f1/{season}/races/') as response:
            if response.status in range(400, 499):
                return None
            response = await response.json()
            response = response['MRData']['RaceTable']['Races']
            races = []
            is_empty = 0
            for race in response:
                roundnumber = race['round']
                name = race['raceName']
                date = race['date']
                try:
                    time = race['time'].replace('Z', '')
                    time = time[:5]
                except:
                    time = None
                if race.get('Sprint'):
                    sprint = True
                else:
                    sprint = None

                if time:
                    if sprint:
                        races.append(f'{roundnumber}. {name} (Sprint) - {date} {time} UTC')
                    else:
                        races.append(f'{roundnumber}. {name} - {date} {time} UTC')
                else:
                    races.append(f'{roundnumber}. {name} - {date} UTC')
                is_empty += 1
            if is_empty == 0:
                return []
            return races


async def f1_standings_py(season: int = CURRENT_YEAR) -> list:
    """
    Fetches the F1 driver standings for a specific season. If 'season' is empty, the current year is used.

    Args:
        season (int): The season to fetch standings for. Defaults to the current year.

    Returns:
        list: A list of strings formatted as 'position. DriverName (Team) - points pts.'.
              Returns an empty list if the request fails or no data is found.
    """
    if season < 1950 or season > CURRENT_YEAR:
        return []
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.jolpi.ca/ergast/f1/{season}/driverstandings/') as response:
            if response.status in range(400, 499):
                return []
            data = await response.json()
            try:
                standings_json = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
            except (KeyError, IndexError):
                return []

            standings_list = []
            for driver in standings_json:
                driver_name = f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}"
                position = driver['position']
                team = driver['Constructors'][0]['name']
                points = driver['points']
                standings_list.append(f'{position}. {driver_name} ({team}) - {points} pts.')
            return standings_list
