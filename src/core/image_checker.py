import aiohttp

IMAGE_CONTENT_TYPES = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
    'image/svg+xml'
]

async def image_checker(session: aiohttp.ClientSession, image_link: str) -> bool:
    """Checks does an image exist.

    Args:
        session (aiohttp.ClientSession)
        image_link (str): Image URL to check.


    Returns:
        bool: True if image exists, None if image does not exist.
    """
    if not image_link:
        return True
    try:
        async with session.head(image_link, timeout=3) as response:
            if response.status != 200:
                return None
            content_type = response.headers.get('Content-Type', '').lower()
            for image_type in IMAGE_CONTENT_TYPES:
                if content_type.startswith(image_type):
                    return True
            return None
    except Exception:
        return None