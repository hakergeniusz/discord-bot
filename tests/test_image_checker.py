import pytest
from unittest.mock import AsyncMock, patch
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
