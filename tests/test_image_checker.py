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

"""Unit tests for the image checker module."""

from unittest.mock import AsyncMock

import aiohttp
import pytest

from src.core.image_checker import image_checker


@pytest.fixture
def mock_session() -> AsyncMock:
    """Fixture for mocking aiohttp.ClientSession."""
    return AsyncMock(spec=aiohttp.ClientSession)


@pytest.mark.asyncio
async def test_image_checker_pass(mock_session: AsyncMock) -> None:
    """Test image checker with a valid image URL."""
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.headers = {"Content-Type": "image/png"}
    mock_session.head.return_value.__aenter__.return_value = mock_response

    result = await image_checker(mock_session, "https://example.com/image.png")
    assert result is True


@pytest.mark.asyncio
async def test_image_checker_not_found(mock_session: AsyncMock) -> None:
    """Test image checker with a non-existent URL."""
    mock_response = AsyncMock()
    mock_response.status = 404
    mock_session.head.return_value.__aenter__.return_value = mock_response

    result = await image_checker(mock_session, "https://example.com/image.png")
    assert result is False


@pytest.mark.asyncio
async def test_image_checker_not_image(mock_session: AsyncMock) -> None:
    """Test image checker with a URL that is not an image."""
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.headers = {"Content-Type": "text/html"}
    mock_session.head.return_value.__aenter__.return_value = mock_response

    result = await image_checker(mock_session, "https://example.com/test.html")
    assert result is False


@pytest.mark.asyncio
async def test_image_checker_timeout(mock_session: AsyncMock) -> None:
    """Test image checker when a timeout occurs."""
    mock_session.head.side_effect = Exception("Timeout")

    result = await image_checker(mock_session, "https://example.com/test.html")
    assert result is False
