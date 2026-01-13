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

from google import genai

gemini_client = genai.Client().aio

async def process_prompt(message: str):
    """
    Sends asynchronously a prompt to Gemma 3 27B and yields chunks of text.

    Args:
        message (str): The prompt from the user.
    Yields:
        str: Text chunks as they arrive from Google.
    """
    response = await gemini_client.models.generate_content_stream(
        contents=f'{message}',
        model="gemma-3-27b-it",
    )
    async for chunk in response:
        if chunk.text:
            yield chunk.text