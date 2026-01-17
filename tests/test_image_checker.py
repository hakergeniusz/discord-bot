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
from unittest.mock import AsyncMock
import aiohttp
from src.core.image_checker import image_checker

@pytest.fixture
def mock_session():
    return AsyncMock(spec=aiohttp.ClientSession)

@pytest.mark.asyncio
async def test_image_checker_pass(mock_session):
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.headers = {'Content-Type': 'image/png'}
    mock_session.head.return_value.__aenter__.return_value = mock_response

    result = await image_checker(mock_session, "https://example.com/image.png")
    assert result is True


@pytest.mark.asyncio
async def test_image_checker_not_found(mock_session):
    mock_response = AsyncMock()
    mock_response.status = 404
    mock_session.head.return_value.__aenter__.return_value = mock_response

    result = await image_checker(mock_session, "https://example.com/image.png")
    assert result is False


@pytest.mark.asyncio
async def test_image_checker_not_image(mock_session):
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.headers = {'Content-Type': 'text/html'}
    mock_session.head.return_value.__aenter__.return_value = mock_response

    result = await image_checker(mock_session, "https://example.com/test.html")
    assert result is False


@pytest.mark.asyncio
async def test_image_checker_timeout(mock_session):
    mock_session.head.side_effect = Exception("Timeout")

    result = await image_checker(mock_session, "https://example.com/test.html")
    assert result is False
