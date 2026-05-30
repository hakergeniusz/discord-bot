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

"""Unit tests for the howmany module."""

from unittest.mock import MagicMock, patch

import pytest

from src.core.howmany import change_file, create_file


@pytest.mark.asyncio
@patch("src.core.howmany.Path.write_text")
@patch("src.core.howmany.Path.exists")
@patch("src.core.howmany.Path.read_text")
async def test_create_file_success(
    mock_read: MagicMock,
    mock_exists: MagicMock,
    mock_write: MagicMock,
) -> None:
    """Test successful file creation."""
    mock_exists.return_value = True
    mock_read.return_value = "test content"

    result = await create_file("test.txt", "test content")

    assert result is True
    mock_write.assert_called_once_with("test content")


@pytest.mark.asyncio
@patch("src.core.howmany.Path.open")
@patch("src.core.howmany.Path.exists")
async def test_create_file_failure(
    mock_exists: MagicMock,
    mock_open: MagicMock,  # noqa: ARG001
) -> None:
    """Test file creation failure when file doesn't exist after writing."""
    mock_exists.return_value = False

    result = await create_file("test.txt", "test content")

    assert result is None


@pytest.mark.asyncio
@patch("src.core.howmany.Path.exists")
@patch("src.core.howmany.Path.write_text")
@patch("src.core.howmany.Path.read_text")
@patch("src.core.howmany.Path.replace")
async def test_change_file_new(
    mock_replace: MagicMock,  # noqa: ARG001
    mock_read: MagicMock,
    mock_write: MagicMock,
    mock_exists: MagicMock,
) -> None:
    """Test incrementing counter for a new user (file doesn't exist)."""
    mock_exists.return_value = False
    mock_read.return_value = "0"

    count = await change_file("test_path", 123)

    assert count == 1
    mock_write.assert_any_call("0")
    mock_write.assert_any_call("1")


@pytest.mark.asyncio
@patch("src.core.howmany.Path.exists")
@patch("src.core.howmany.Path.read_text")
@patch("src.core.howmany.Path.write_text")
@patch("src.core.howmany.Path.replace")
async def test_change_file_existing(
    mock_replace: MagicMock,
    mock_write: MagicMock,
    mock_read: MagicMock,
    mock_exists: MagicMock,
) -> None:
    """Test incrementing counter for an existing user."""
    mock_exists.return_value = True
    mock_read.return_value = "5"

    count = await change_file("test_path", 123)

    assert count == 6
    mock_write.assert_called_once_with("6")
    mock_replace.assert_called_once()
