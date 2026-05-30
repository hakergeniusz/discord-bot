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

"""Module for verifying if a URL points to a valid image."""

import aiohttp
from aiohttp import ClientTimeout

from core.config import NORESPONSE_SUCCESS_RESPONSE_CODE
from core.logger import get_logger

logger = get_logger(__name__)

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
        timeout = ClientTimeout(total=3)
        async with session.head(image_link, timeout=timeout) as response:
            if response.status != NORESPONSE_SUCCESS_RESPONSE_CODE:
                return False
            content_type = response.headers.get("Content-Type", "").lower()
            return any(content_type.startswith(image_type) for image_type in IMAGE_CONTENT_TYPES)
    except Exception:
        logger.exception("Error checking image")
        return False
