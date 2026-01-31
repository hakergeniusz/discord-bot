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

from unittest.mock import MagicMock, patch

import pytest

from src.core.howmany import change_file, create_file


@pytest.mark.asyncio
@patch("src.core.howmany.Path.write_text")
@patch("src.core.howmany.Path.exists")
@patch("src.core.howmany.Path.read_text")
async def test_create_file_success(
    mock_read: MagicMock, mock_exists: MagicMock, mock_write: MagicMock
) -> None:
    """Test successful file creation."""
    mock_exists.return_value = True
    mock_read.return_value = "test content"

    result = await create_file("test.txt", "test content")

    assert result is True
    mock_write.assert_called_once_with("test content")


@pytest.mark.asyncio
@patch("src.core.howmany.Path.write_text")
@patch("src.core.howmany.Path.exists")
async def test_create_file_failure(
    mock_exists: MagicMock, mock_write: MagicMock
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
    mock_replace: MagicMock,
    mock_read: MagicMock,
    mock_write: MagicMock,
    mock_exists: MagicMock,
) -> None:
    """Test incrementing counter for a new user (file doesn't exist)."""
    mock_exists.return_value = False
    mock_read.return_value = "0"

    count = await change_file("/tmp", 123)

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

    count = await change_file("/tmp", 123)

    assert count == 6
    mock_write.assert_called_once_with("6")
    mock_replace.assert_called_once()
