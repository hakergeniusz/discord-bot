# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Module for interacting with Google's Gemma AI models."""

from typing import TYPE_CHECKING

from google import genai
from google.genai import errors as gemini_errors

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

gemini_client = genai.Client().aio


async def process_prompt(message: str) -> AsyncGenerator[str]:
    """Sends asynchronously a prompt to Gemma 4 31B and yields chunks of text.

    Args:
        message (str): The prompt from the user.

    Yields:
        str: Text chunks as they arrive from Google.
    """
    try:
        response = await gemini_client.models.generate_content_stream(
            contents=f"{message}",
            model="gemma-4-31b-it",
        )
        async for chunk in response:
            if chunk.text:
                yield chunk.text
    except gemini_errors.ServerError:
        yield "An unknown error has occured. Please try again in a minute."
