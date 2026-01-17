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

import pytest
from unittest.mock import AsyncMock, patch
from src.core.f1 import race_result, f1_season_calendar, f1_standings_py
from src.core.config import CURRENT_YEAR

@pytest.mark.asyncio
async def test_f1_standings_py_success():
    mock_data = {
        "MRData": {
            "StandingsTable": {
                "StandingsLists": [
                    {
                        "DriverStandings": [
                            {
                                "position": "1",
                                "points": "25",
                                "Driver": {"givenName": "Max", "familyName": "Verstappen"},
                                "Constructors": [{"name": "Red Bull"}]
                            }
                        ]
                    }
                ]
            }
        }
    }

    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value.__aenter__.return_value = mock_response

        result = await f1_standings_py(2024)

        assert len(result) == 1
        assert "1. Max Verstappen (Red Bull) - 25 pts." in result

@pytest.mark.asyncio
async def test_f1_standings_py_empty():
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 404
        mock_get.return_value.__aenter__.return_value = mock_response

        result = await f1_standings_py(2024)
        assert result == []

@pytest.mark.asyncio
async def test_f1_race_result_success():
    mock_data = {
        "MRData": {
            "RaceTable": {
                "Races": [
                    {
                        "raceName": "British Grand Prix",
                        "Results": [
                            {
                                "position": "1",
                                "Driver": {"givenName": "Lewis", "familyName": "Hamilton"},
                                "Constructor": {"name": "Mercedes"},
                                "status": "Finished"
                            }
                        ]
                    }
                ]
            }
        }
    }

    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value.__aenter__.return_value = mock_response

        gp_name, results = await race_result(2024, 12)

        assert gp_name == "British Grand Prix"
        assert "🥇 Lewis Hamilton (Mercedes)" in results[0]


@pytest.mark.asyncio
async def test_f1_race_result_no_emojis():
    mock_data = {
        "MRData": {
            "RaceTable": {
                "Races": [
                    {
                        "raceName": "British Grand Prix",
                        "Results": [
                            {
                                "position": "1",
                                "Driver": {"givenName": "Lewis", "familyName": "Hamilton"},
                                "Constructor": {"name": "Mercedes"},
                                "status": "Finished"
                            }
                        ]
                    }
                ]
            }
        }
    }

    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value.__aenter__.return_value = mock_response

        gp_name, results = await race_result(2024, 12, emojis=False)

        assert gp_name == "British Grand Prix"
        assert "1. Lewis Hamilton (Mercedes)" in results[0]


@pytest.mark.asyncio
async def test_f1_season_calendar_success():
    mock_data = {
        "MRData": {
            "RaceTable": {
                "Races": [
                    {
                        "round": "1",
                        "raceName": "Australian Grand Prix",
                        "date": "2026-03-08",
                        "time": "04:00:00Z"
                    }
                ]
            }
        }
    }

    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value.__aenter__.return_value = mock_response

        races = await f1_season_calendar(2025)

        assert races[0] == "1. Australian Grand Prix - 2026-03-08 04:00 UTC"


@pytest.mark.asyncio
async def test_f1_season_calendar_no_hour():
    mock_data = {
        "MRData": {
            "RaceTable": {
                "Races": [
                    {
                        "round": "1",
                        "raceName": "Australian Grand Prix",
                        "date": "2026-03-08",
                    }
                ]
            }
        }
    }

    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value.__aenter__.return_value = mock_response

        races = await f1_season_calendar(2025)

        assert races[0] == "1. Australian Grand Prix - 2026-03-08 UTC"


@pytest.mark.asyncio
async def test_f1_season_calendar_sprint():
    mock_data = {
        "MRData": {
            "RaceTable": {
                "Races": [
                    {
                        "round": "2",
                        "raceName": "Chinese Grand Prix",
                        "date": "2026-03-15",
                        "time": "07:00:00Z",
                        "Sprint": {"date": "2026-03-14","time": "03:00:00Z"},
                    }
                ]
            }
        }
    }

    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value.__aenter__.return_value = mock_response

        races = await f1_season_calendar(2025)

        assert races[0] == "2. Chinese Grand Prix (Sprint) - 2026-03-15 07:00 UTC"


@pytest.mark.asyncio
async def test_f1_standings_py_invalid_year():
    standings1 = await f1_standings_py(1949)
    assert standings1 == []
    next_year = CURRENT_YEAR + 1
    standings2 = await f1_standings_py(next_year)
    assert standings2 == []
