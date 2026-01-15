import pytest
from unittest.mock import AsyncMock, patch
import aiohttp
from src.core.f1 import race_result, f1_season_calendar, f1_standings_py

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
