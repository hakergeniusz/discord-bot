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

"""Unit tests for the F1 core module."""

from unittest.mock import AsyncMock, patch

import pytest

from src.core.config import CURRENT_YEAR
from src.core.f1 import (
    f1_qualifying,
    f1_season_calendar,
    f1_standings_py,
    identify_qualifying_session,
    race_result,
)


@pytest.mark.asyncio
async def test_f1_qualifying_success() -> None:
    """Test successful fetching of qualifying results."""
    mock_data = {
        "MRData": {
            "RaceTable": {
                "Races": [
                    {
                        "raceName": "Australian Grand Prix",
                        "QualifyingResults": [
                            {
                                "position": "1",
                                "Driver": {
                                    "givenName": "George",
                                    "familyName": "Russell",
                                },
                                "Constructor": {"name": "Mercedes"},
                                "Q1": "1:19.507",
                                "Q2": "1:18.934",
                                "Q3": "1:18.518",
                            },
                            {
                                "position": "11",
                                "Driver": {
                                    "givenName": "Nico",
                                    "familyName": "Hülkenberg",
                                },
                                "Constructor": {"name": "Haas"},
                                "Q1": "1:21.024",
                                "Q2": "1:20.303",
                            },
                            {
                                "position": "17",
                                "Driver": {
                                    "givenName": "Fernando",
                                    "familyName": "Alonso",
                                },
                                "Constructor": {"name": "Aston Martin"},
                                "Q1": "1:21.969",
                            },
                        ],
                    },
                ],
            },
        },
    }

    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value.__aenter__.return_value = mock_response

        gp_name, results = await f1_qualifying(2026, 1)

        assert gp_name == "Australian Grand Prix"
        assert len(results) == 3
        assert "1. George Russell (Mercedes) - Q3" in results[0]
        assert "11. Nico Hülkenberg (Haas) - Q2" in results[1]
        assert "17. Fernando Alonso (Aston Martin) - Q1" in results[2]


def test_identify_qualifying_session() -> None:
    """Test identifying the furthest qualifying session."""
    assert identify_qualifying_session({"Q1": "1:20", "Q2": "1:19", "Q3": "1:18"}) == "Q3"
    assert identify_qualifying_session({"Q1": "1:20", "Q2": "1:19"}) == "Q2"
    assert identify_qualifying_session({"Q1": "1:20"}) == "Q1"


@pytest.mark.asyncio
async def test_f1_standings_py_success() -> None:
    """Test successful fetching of driver standings."""
    mock_data = {
        "MRData": {
            "StandingsTable": {
                "StandingsLists": [
                    {
                        "DriverStandings": [
                            {
                                "position": "1",
                                "points": "25",
                                "Driver": {
                                    "givenName": "Max",
                                    "familyName": "Verstappen",
                                },
                                "Constructors": [{"name": "Red Bull"}],
                            },
                        ],
                    },
                ],
            },
        },
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
async def test_f1_standings_py_empty() -> None:
    """Test driver standings with empty response."""
    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 404
        mock_get.return_value.__aenter__.return_value = mock_response

        result = await f1_standings_py(2024)
        assert result == []


@pytest.mark.asyncio
async def test_f1_race_result_success() -> None:
    """Test successful fetching of race results."""
    mock_data = {
        "MRData": {
            "RaceTable": {
                "Races": [
                    {
                        "raceName": "British Grand Prix",
                        "Results": [
                            {
                                "position": "1",
                                "Driver": {
                                    "givenName": "Lewis",
                                    "familyName": "Hamilton",
                                },
                                "Constructor": {"name": "Mercedes"},
                                "status": "Finished",
                            },
                        ],
                    },
                ],
            },
        },
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
async def test_f1_race_result_no_emojis() -> None:
    """Test race results without emojis."""
    mock_data = {
        "MRData": {
            "RaceTable": {
                "Races": [
                    {
                        "raceName": "British Grand Prix",
                        "Results": [
                            {
                                "position": "1",
                                "Driver": {
                                    "givenName": "Lewis",
                                    "familyName": "Hamilton",
                                },
                                "Constructor": {"name": "Mercedes"},
                                "status": "Finished",
                            },
                        ],
                    },
                ],
            },
        },
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
async def test_f1_season_calendar_success() -> None:
    """Test successful fetching of season calendar."""
    mock_data = {
        "MRData": {
            "RaceTable": {
                "Races": [
                    {
                        "round": "1",
                        "raceName": "Australian Grand Prix",
                        "date": "2026-03-08",
                        "time": "04:00:00Z",
                    },
                ],
            },
        },
    }

    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value.__aenter__.return_value = mock_response

        races = await f1_season_calendar(2025)

        assert races[0] == "1. Australian Grand Prix - 2026-03-08 04:00 UTC"


@pytest.mark.asyncio
async def test_f1_season_calendar_no_hour() -> None:
    """Test season calendar when time is missing."""
    mock_data = {
        "MRData": {
            "RaceTable": {
                "Races": [
                    {
                        "round": "1",
                        "raceName": "Australian Grand Prix",
                        "date": "2026-03-08",
                    },
                ],
            },
        },
    }

    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value.__aenter__.return_value = mock_response

        races = await f1_season_calendar(2025)

        assert races[0] == "1. Australian Grand Prix - 2026-03-08 UTC"


@pytest.mark.asyncio
async def test_f1_season_calendar_sprint() -> None:
    """Test season calendar with sprint races."""
    mock_data = {
        "MRData": {
            "RaceTable": {
                "Races": [
                    {
                        "round": "2",
                        "raceName": "Chinese Grand Prix",
                        "date": "2026-03-15",
                        "time": "07:00:00Z",
                        "Sprint": {"date": "2026-03-14", "time": "03:00:00Z"},
                    },
                ],
            },
        },
    }

    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = mock_data
        mock_get.return_value.__aenter__.return_value = mock_response

        races = await f1_season_calendar(2025)

        assert races[0] == "2. Chinese Grand Prix (Sprint) - 2026-03-15 07:00 UTC"


@pytest.mark.asyncio
async def test_f1_standings_py_invalid_year() -> None:
    """Test driver standings with invalid years."""
    standings1 = await f1_standings_py(1949)
    assert standings1 == []
    next_year = CURRENT_YEAR + 1
    standings2 = await f1_standings_py(next_year)
    assert standings2 == []
