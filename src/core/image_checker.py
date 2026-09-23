# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

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
