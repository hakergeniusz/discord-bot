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