# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Unit tests for the image checker module."""

from unittest.mock import AsyncMock

import aiohttp
import pytest

from src.core.image_checker import image_checker


@pytest.fixture
def mock_session() -> AsyncMock:
    """Fixture for mocking aiohttp.ClientSession.

    Returns:
        AsyncMock: A mocked aiohttp.ClientSession object.
    """
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


@pytest.mark.asyncio
async def test_image_checker_no_link(mock_session: AsyncMock) -> None:
    """Test image checker with empty link input."""
    empty_input = ""
    result = await image_checker(mock_session, empty_input)
    assert result is False
