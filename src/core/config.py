#  Copyright (C) 2026 hakergeniusz
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import aiohttp
import asyncio
import fastf1
import discord
from discord.ext import commands
from discord import app_commands
from google import genai
import datetime
import yt_dlp
import re
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TMP_BASE = os.path.join(PROJECT_ROOT, "tmp")

OWNER_ID = int(os.environ.get('DISCORD_OWNER_ID'))
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

PC_POWEROFF = os.environ.get('POWEROFF_COMMAND')
if PC_POWEROFF != 'True':
    PC_POWEROFF = None

CURRENT_YEAR = datetime.date.today().year

IMAGE_CONTENT_TYPES = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
    'image/svg+xml'
]

status_map = {
    "Lapped": "Lapped",
    "Retired": "DNF",
    "Accident": "DNF (Accident)",
    "Collision": "DNF (Collision)",
    "Spun off": "DNF (Spin)",
    "Not classified": "NC",
    "Gearbox": "DNF (Gearbox)",
    "Engine": "DNF (Engine)",
    "Transmission": "DNF (Transmission)",
    "Electrical": "DNF (Electrical)",
    "Out of fuel": "DNF (Fuel)",
    "Oil leak": "DNF (Oil)",
    "Brakes": "DNF (Brakes)",
    "Suspension": "DNF (Suspension)",
    "Tyre": "DNF (Tyre)",
    "Cooling": "DNF (Cooling)",
    "Did not start": "DNS",
    "Withdrew": "DNS",
    "Injury": "DNS",
    "Illness": "DNS",
    "Disqualified": "DSQ",
    "Oil pressure": "DNF (Oil)",
    "Clutch": "DNF (Clutch)",
    "Supercharger": "DNF (Supercharger)",
    "Hydraulics": "DNF (Hydraulics)"
}

ydl_opts = {
    'outtmpl': '/tmp/%(id)s.%(ext)s',
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'opus',
        'preferredquality': '128',
    }],
}

youtube_regex = (
        r'(https?://)?(www\.|m\.)?'
        r'(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)'
        r'([\w-]{11})'
    )

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


async def find_circuit(season: int, roundnumber: int) -> str:
    """
    Finds an F1 circuit name.

    Args:
        season (int): Season where the race was.
        roundnumber (int): Round number of the race to return the name.

    Returns:
        str: Circuit's name if it existed.
        bool: None, if circuit not found.
    """
    schedule = await asyncio.to_thread(fastf1.get_event_schedule, season)
    row = schedule.loc[schedule['RoundNumber'] == roundnumber]

    if not row.empty:
        event_name = row.iloc[0]['EventName']
        return f"{event_name}"
    else:
        return None


async def does_exist(season: int, roundnumber: int) -> bool:
    """Checks did an F1 race historically exist or not.

    Args:
        season (int)
        roundnumber (int): Race number in F1 calendar to check.

    Returns:
        bool: True if existed, None if it did not exist.
    """
    schedule = await asyncio.to_thread(fastf1.get_event_schedule, season)
    event_row = schedule.loc[schedule['RoundNumber'] == roundnumber]
    if event_row.empty:
        return None
    else:
        return True

def cowsay(text: str) -> str:
    """
    A simple cowsay.

    Args:
        text (str): Text for the cow to say.

    Returns:
        str: Cow in a code block that says the *text* argument.
    """
    if text is None:
        return
    length = len(text)
    top_bottom =  " " + "_" * (length + 2)
    bubble_text = f"< {text} >"
    cow = fr"""
```
{top_bottom}
{bubble_text}
 {('-' * (length + 2))}
        \   ^__^
         \  (oo)\_______
            (__)\       )\\/\\
                ||----w |
                ||     ||
```
    """
    return cow


def admin_check() -> commands.check:
    """
    Checks does the author of the context (ctx) have admin permissions. Works with prefix and hybrid commands. Does not work with slash only commands.

    Returns:
        commands.check: A decorator that can be used to easily protect bot commands.

    Implementation:
        Add @admin_check() at start of command's code.
    """
    async def predicate(ctx):
        user = getattr(ctx, 'author', getattr(ctx, 'user', None))

        if user and user.id == OWNER_ID:
            return True

        msg = "You don't have required permissions to do that."
        if hasattr(ctx, 'send'):
            message = await ctx.send(msg)
            await asyncio.sleep(3)
            await ctx.message.delete()
            await message.delete()
        else:
            await ctx.response.send_message(msg, ephemeral=True)

        return False
    return commands.check(predicate)


def admin_check_slash():
    """
    Checks does the author of the interaction have admin permissions. Works only with slash commands.

    Returns:
        commands.check: A decorator that can be used to easily protect bot commands.

    Implementation:
        Add @admin_check() at start of command's code.
    """
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.user.id == OWNER_ID:
            return True
        await interaction.response.send_message("You don't have required permissions to do that.", ephemeral=True)
        return False
    return app_commands.check(predicate)



def download_youtube_video(url: str):
    """
    Downloads a YouTube video from the given URL and returns the path to the downloaded file.

    Args:
        url (str): The URL of the YouTube video to be downloaded.

    Returns:
        str: The path to the downloaded file with the extension changed to .opus.
        bool: If the video could not be downloaded or video not found.
    """
    match = re.match(youtube_regex, url)
    if not bool(match):
        return None
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            path = ydl.prepare_filename(info).replace(".webm", ".opus").replace(".m4a", ".opus")
            if os.path.exists(path):
                return path
            else:
                return None
    except Exception:
        return None