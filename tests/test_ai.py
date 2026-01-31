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
    "src.core.ai.gemini_client.models.generate_content_stream", new_callable=AsyncMock
)
async def test_process_prompt_success(mock_generate: AsyncMock) -> None:
    """Test successful processing of a prompt yielding multiple chunks."""
    chunks = [MockChunk("Hello"), MockChunk(" "), MockChunk("world!")]

    mock_response = AsyncMock()
    mock_response.__aiter__.return_value = chunks
    mock_generate.return_value = mock_response

    result_chunks = []
    async for chunk in process_prompt("hi"):
        result_chunks.append(chunk)

    assert result_chunks == ["Hello", " ", "world!"]
    mock_generate.assert_called_once_with(contents="hi", model="gemma-3-27b-it")


@pytest.mark.asyncio
@patch(
    "src.core.ai.gemini_client.models.generate_content_stream", new_callable=AsyncMock
)
async def test_process_prompt_empty_chunks(mock_generate: AsyncMock) -> None:
    """Test that empty chunks are skipped."""
    chunks = [MockChunk("Hello"), MockChunk(None), MockChunk("world!")]

    mock_response = AsyncMock()
    mock_response.__aiter__.return_value = chunks
    mock_generate.return_value = mock_response

    result_chunks = []
    async for chunk in process_prompt("hi"):
        result_chunks.append(chunk)

    assert result_chunks == ["Hello", "world!"]
