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

"""Module for tracking command usage counts in temporary (or not) files."""

import asyncio
from pathlib import Path
from typing import Optional

from core.config import TMP_BASE

file_lock = asyncio.Lock()


async def create_file(file_name: str, file_content: str) -> Optional[bool]:
    """Creates a file with requested name in TMP subfolder.

    Args:
        file_name: The file name to create with the extension.
        file_content: Content of the file to write.

    Returns:
        bool: True if file is written successfully, None if it isn't.
    """
    path = Path(TMP_BASE) / file_name
    path.write_text(file_content)

    if not path.exists():
        return None

    if path.read_text() == file_content:
        return True
    return None


async def change_file(path: str, user_id: int) -> int:
    """Adds 1 to the number in a file. If there is no file, a new file is created.

    Args:
        path: Folder where the file is in.
        user_id: Discord user ID of the user that triggered the command.

    Returns:
        int: New number that is in the file.
    """
    orig_path = Path(path) / f"{user_id}.txt"
    new_path = orig_path.with_suffix(".txt.new")
    async with file_lock:
        if not orig_path.exists():
            orig_path.write_text("0")

        count = int(orig_path.read_text())
        new_count = count + 1
        new_path.write_text(str(new_count))
        new_path.replace(orig_path)
        return new_count
