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

import os
from core.config import TMP_BASE

async def create_file(file_name: str, file_content: str) -> bool:
    """
    Creates a file with requested name in TMP subfolder.

    Args:
        file_name (str): The file name to create with the extension.
        file_content (str): Content of the file to write.

    Returns:
        bool: True if file is written successfully, None if it isn't.
    """
    PATH = os.path.join(TMP_BASE, f'{file_name}')
    with open(PATH, 'w') as f:
        f.write(f'{file_content}')

    if not os.path.exists(PATH):
        return None

    with open(PATH, 'r') as f:
        if f.read() == file_content:
            return True
        else:
            return None


def change_file(path: int, id: int) -> int:
    """
    Adds 1 to the number in a file. If there is no file, a new file is created.

    Args:
        path (str): Folder where the file is in.
        id (int): Discord user ID of the user that triggered the command.

    Returns:
        int: New number that is in the file.
    """
    FILE_PATH = os.path.join(path, f'{id}.txt')
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'w') as f:
            f.write('0')

    with open(FILE_PATH, 'r') as f:
        count = int(f.read())

    with open(FILE_PATH, 'w') as f:
        f.write(f'{count + 1}')
        return count + 1