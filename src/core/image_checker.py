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

"""Module for verifying if a URL points to a valid image."""

import aiohttp

IMAGE_CONTENT_TYPES = [
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "image/svg+xml",
]


async def image_checker(session: aiohttp.ClientSession, image_link: str) -> bool:
    """Checks does an image exist.

    Args:
        session (aiohttp.ClientSession): The aiohttp session to use for the check.
        image_link (str): Image URL to check.


    Returns:
        bool: True if image exists, False if image does not exist.
    """
    if not image_link:
        return False
    try:
        async with session.head(image_link, timeout=3) as response:
            if response.status != 200:
                return False
            content_type = response.headers.get("Content-Type", "").lower()
            for image_type in IMAGE_CONTENT_TYPES:
                if content_type.startswith(image_type):
                    return True
            return False
    except Exception:
        return False
