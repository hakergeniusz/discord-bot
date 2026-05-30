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

"""Unit tests for the AI core module."""

from unittest.mock import AsyncMock, patch

import pytest

with patch("google.genai.Client"):
    from src.core.ai import process_prompt


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
    mock_generate.assert_called_once_with(contents="hi", model="gemma-4-26b-a4b-it")


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
