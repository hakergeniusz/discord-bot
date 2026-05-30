# Copyright (c) 2025-2026 hakergeniusz
#
# Licensed under the EUPL, Version 1.2 or - as soon they will be approved by the European
# Commission - subsequent versions of the EUPL (the "Licence"); You may not use this work
# except in compliance with the Licence.
#
# You may obtain a copy of the Licence at:
# https://joinup.ec.europa.eu/software/page/eupl
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the Licence for the specific language
# governing permissions and limitations under the Licence.

"""Module for fetching Formula 1 data using the Jolpica API."""

import aiohttp

from core.config import CURRENT_YEAR, F1_FIRST_YEAR, STATUS_MAP


async def race_result(
    season: int,
    roundnumber: int,
    *,
    emojis: bool = True,
) -> tuple[str | None, list[str]]:
    """Gives the result of an F1 race session using Jolpica API.

    Args:
        season (int): The season to fetch results for.
        roundnumber (int): Race number in F1 calendar to check.
        emojis (bool): Default is True. If False, emojis for first three positions
            will not be given.

    Returns:
        tuple[str | None, list[str]]: Circuit's name and a list with session results.
    """
    async with (
        aiohttp.ClientSession() as session,
        session.get(
            f"https://api.jolpi.ca/ergast/f1/{season}/{roundnumber}/results/",
        ) as response,
    ):
        if response.status in range(400, 499):
            return None, []

        data = await response.json()
        data = data["MRData"]["RaceTable"]["Races"]
        if data == []:
            return None, []
        circuit_name = data[0]["raceName"]
        results = []
        for result in data[0]["Results"]:
            pos = result["position"]
            if emojis:
                if pos == "1":
                    pos = "🥇"
                elif pos == "2":
                    pos = "🥈"
                elif pos == "3":
                    pos = "🥉"
                else:
                    pos = f"{pos}."
            else:
                pos = f"{pos}."
            driver_name = result["Driver"]["givenName"] + " " + result["Driver"]["familyName"]
            team = result["Constructor"]["name"]
            status = result["status"]
            status = STATUS_MAP.get(status, status)
            if status == "Finished":
                results.append(f"{pos} {driver_name} ({team})")
            else:
                results.append(f"{pos} {driver_name} ({team}) - {status}")

        return circuit_name, results


async def f1_qualifying(season: int, roundnumber: int) -> tuple[str | None, list[str]]:
    """Gives the result of an F1 qualifying session using Jolpica API.

    Args:
        season (int): The season to fetch results for.
        roundnumber (int): Race number in F1 calendar to check.

    Returns:
        tuple[str | None, list[str]]: Circuit's name and a list with session results.
    """
    async with (
        aiohttp.ClientSession() as session,
        session.get(
            f"https://api.jolpi.ca/ergast/f1/{season}/{roundnumber}/qualifying/",
        ) as response,
    ):
        if response.status in range(400, 499):
            return None, []

        data = await response.json()
        data = data["MRData"]["RaceTable"]["Races"]
        if data == []:
            return None, []
        circuit_name = data[0]["raceName"]
        results = []
        for result in data[0]["QualifyingResults"]:
            driver_name = result["Driver"]["givenName"] + " " + result["Driver"]["familyName"]
            team = result["Constructor"]["name"]
            session_out = identify_qualifying_session(result)
            set_time = result[session_out]
            results.append(
                f"{result['position']}. {driver_name} ({team}) - {session_out} {set_time}",
            )

        return circuit_name, results


def identify_qualifying_session(driver_data: dict) -> str:
    """Identifies the furthest qualifying session reached by a driver.

    Args:
        driver_data (dict): The driver's qualifying data from the API.

    Returns:
        str: The session name ("Q1", "Q2", or "Q3").
    """
    if "Q3" in driver_data:
        return "Q3"
    if "Q2" in driver_data:
        return "Q2"
    return "Q1"


async def f1_season_calendar(season: int) -> list[str]:
    """Gives the F1 calendar using Jolpica API.

    Args:
        season (int): Season to find the calendar for.

    Returns:
        list: A list with all races in the season.
    """
    async with (
        aiohttp.ClientSession() as session,
        session.get(
            f"https://api.jolpi.ca/ergast/f1/{season}/races/",
        ) as response,
    ):
        if response.status in range(400, 499):
            return []
        data = await response.json()
        data = data["MRData"]["RaceTable"]["Races"]
        races = []
        is_empty = 0
        for race in data:
            roundnumber = race["round"]
            name = race["raceName"]
            date = race["date"]
            try:
                time = race["time"].replace("Z", "")
                time = time[:5]
            except KeyError, TypeError, ValueError:
                time = None
            sprint = True if race.get("Sprint") else None

            if time:
                if sprint:
                    races.append(
                        f"{roundnumber}. {name} (Sprint) - {date} {time} UTC",
                    )
                else:
                    races.append(f"{roundnumber}. {name} - {date} {time} UTC")
            else:
                races.append(f"{roundnumber}. {name} - {date} UTC")
            is_empty += 1
        if is_empty == 0:
            return []
        return races


async def f1_standings_py(season: int = CURRENT_YEAR) -> list[str]:
    """Fetches the F1 driver standings for a specific season.

    If 'season' is empty, the current year is used.

    Args:
        season (int): The season to fetch standings for. Defaults to the current year.

    Returns:
        list: A list of strings formatted as
              'position. DriverName (Team) - points pts.'.
              Returns an empty list if the request fails or no data is found.
    """
    if season < F1_FIRST_YEAR or season > CURRENT_YEAR:
        return []
    async with (
        aiohttp.ClientSession() as session,
        session.get(
            f"https://api.jolpi.ca/ergast/f1/{season}/driverstandings/",
        ) as response,
    ):
        if response.status in range(400, 499):
            return []
        data = await response.json()
        try:
            standings_table = data["MRData"]["StandingsTable"]
            standings_json = standings_table["StandingsLists"][0]["DriverStandings"]
        except KeyError, IndexError:
            return []

        standings_list = []
        for driver in standings_json:
            driver_name = f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}"
            position = driver["position"]
            team = driver["Constructors"][0]["name"]
            points = driver["points"]
            standings_list.append(
                f"{position}. {driver_name} ({team}) - {points} pts.",
            )
        return standings_list
