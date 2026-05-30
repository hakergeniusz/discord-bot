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

"""Module for tracking command usage counts in temporary (or not) files."""

import asyncio
from pathlib import Path

from core.config import TMP_BASE

file_lock = asyncio.Lock()


async def create_file(file_name: str, file_content: str) -> bool | None:
    """Creates a file with requested name in TMP subfolder.

    Args:
        file_name: The file name to create with the extension.
        file_content: Content of the file to write.

    Returns:
        bool: True if file is written successfully, None if it isn't.
    """
    path = Path(file_name)
    if not path.is_absolute():
        path = Path(TMP_BASE) / file_name

    path.parent.mkdir(parents=True, exist_ok=True)
    await asyncio.to_thread(path.write_text, file_content)

    if not path.exists():
        return None

    content = await asyncio.to_thread(path.read_text)
    if content == file_content:
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
    dir_path = Path(path)
    if not dir_path.is_absolute():
        dir_path = Path(TMP_BASE) / path

    dir_path.mkdir(parents=True, exist_ok=True)
    orig_path = dir_path / f"{user_id}.txt"
    new_path = orig_path.with_suffix(".txt.new")

    async with file_lock:
        if not orig_path.exists():
            await asyncio.to_thread(orig_path.write_text, "0")

        content = await asyncio.to_thread(orig_path.read_text)
        count = int(content)
        new_count = count + 1
        await asyncio.to_thread(new_path.write_text, str(new_count))
        await asyncio.to_thread(new_path.replace, orig_path)
        return new_count
