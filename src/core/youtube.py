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

import yt_dlp
import re
import os

ydl_opts = {
    'outtmpl': '/tmp/%(id)s.%(ext)s',
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': False,
    'no_warnings': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'source_address': '0.0.0.0',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'opus',
        'preferredquality': '192',
    }],
}

youtube_regex1 = (
        r'(https?://)?(www\.|m\.)?'
        r'(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)'
        r'([\w-]{11})'
)

def get_yt_video_id(url: str) -> str:
    """
    Gives YouTube video ID from a link.

    Args:
        url (str): The URL of the YouTube video.

    Returns:
        str: YouTube video ID.
        bool: None if ID could not be extracted.
    """
    youtube_regex2 = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"

    match = re.search(youtube_regex2, url)
    if match:
        return match.group(1)
    return None

def download_youtube_video(url: str):
    """
    Downloads a YouTube video from the given URL and returns the path to the downloaded file.

    Args:
        url (str): The URL of the YouTube video to be downloaded.

    Returns:
        str: The path to the downloaded file with the extension changed to .opus.
        bool: If the video could not be downloaded or video not found.
    """
    match = re.match(youtube_regex1, url)
    if not bool(match):
        return None
    video_id = get_yt_video_id(url)
    if video_id:
        if os.path.exists(f'/tmp/{video_id}.opus'):
            return f'/tmp/{video_id}.opus'
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
