# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Unit tests for the AI core module."""

from unittest.mock import AsyncMock, patch

import pytest

with patch("google.genai.Client"):
    from src.core.ai import process_prompt

from google.genai import errors as gemini_errors


class MockChunk:
    """Mock class for a chunk of text from the AI."""

    def __init__(self, text: str | None) -> None:
        """Initialize the mock chunk."""
        self.text = text


@pytest.mark.asyncio
@patch(
    "src.core.ai.gemini_client.models.generate_content_stream",
    new_callable=AsyncMock,
)
async def test_process_prompt_success(mock_generate: AsyncMock) -> None:
    """Test successful processing of a prompt yielding multiple chunks."""
    chunks = [MockChunk("Hello"), MockChunk(" "), MockChunk("world!")]

    mock_response = AsyncMock()
    mock_response.__aiter__.return_value = chunks
    mock_generate.return_value = mock_response

    result_chunks = [chunk async for chunk in process_prompt("hi")]

    assert result_chunks == ["Hello", " ", "world!"]
    mock_generate.assert_called_once_with(contents="hi", model="gemma-4-31b-it")


@pytest.mark.asyncio
@patch(
    "src.core.ai.gemini_client.models.generate_content_stream",
    new_callable=AsyncMock,
)
async def test_process_prompt_empty_chunks(mock_generate: AsyncMock) -> None:
    """Test that empty chunks are skipped."""
    chunks = [MockChunk("Hello"), MockChunk(None), MockChunk("world!")]

    mock_response = AsyncMock()
    mock_response.__aiter__.return_value = chunks
    mock_generate.return_value = mock_response

    result_chunks = [chunk async for chunk in process_prompt("hi")]
    assert result_chunks == ["Hello", "world!"]


@pytest.mark.asyncio
@patch(
    "src.core.ai.gemini_client.models.generate_content_stream",
    new_callable=AsyncMock,
)
async def test_servererror(mock_generate: AsyncMock) -> None:
    """Test that error is yield after a ServerError from Google AI Studio."""
    mock_generate.side_effect = gemini_errors.ServerError(
        500,
        {"error": {"message": "Our massive TPU cluster has decided to say 'Liberum Veto'."}},
    )

    reply = [chunk async for chunk in process_prompt("hi")]
    assert reply == ["An unknown error has occured. Please try again in a minute."]
