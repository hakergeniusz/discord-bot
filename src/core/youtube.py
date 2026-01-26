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

import re
from pathlib import Path
from typing import Optional

import yt_dlp

ydl_opts = {
    "outtmpl": "/tmp/%(id)s.%(ext)s",
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": False,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "source_address": "0.0.0.0",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "opus",
            "preferredquality": "192",
        }
    ],
}

youtube_regex1 = (
    r"(https?://)?(www\.|m\.)?"
    r"(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)"
    r"([\w-]{11})"
)


def get_yt_video_id(url: str) -> Optional[str]:
    """Gives YouTube video ID from a link.

    Args:
        url (str): The URL of the YouTube video.

    Returns:
        YouTube video ID, or None if ID could not be extracted.
    """
    youtube_regex2 = (
        r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|"
        r"youtu\.be\/)([^\"&?\/\s]{11})"
    )

    match = re.search(youtube_regex2, url)
    if match:
        return match.group(1)
    return None


def format_duration(seconds: int) -> str:
    """Formats the duration of a YouTube video in a human-readable format.

    Args:
        seconds (int): The duration of the video in seconds.

    Returns:
        str: The duration of the video in a human-readable format.
    """
    if seconds < 60:
        return f"{seconds} seconds"

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    parts = []
    if hours > 0:
        parts.append(f"{hours} {'hour' if hours == 1 else 'hours'}")
    if minutes > 0:
        parts.append(f"{minutes} {'minute' if minutes == 1 else 'minutes'}")
    if seconds > 0:
        parts.append(f"{seconds} {'second' if seconds == 1 else 'seconds'}")

    return " ".join(parts)


def download_youtube_video(
    url: str,
) -> tuple[Optional[str], Optional[str], Optional[str]]:
    """Downloads a YouTube video from the given URL.

    Returns the path to the downloaded file, title, and duration.

    Args:
        url (str): The URL of the YouTube video to be downloaded.

    Returns:
        tuple[Optional[str], Optional[str], Optional[int]]:
            (path, title, duration) or (None, None, None) if failed.
    """
    match = re.match(youtube_regex1, url)
    if not bool(match):
        return None, None, None

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get("title")
            duration = info.get("duration")
            video_id = info.get("id")

            if not video_id:
                return None, None, None

            video_path = Path(f"/tmp/{video_id}.opus")
            if video_path.exists():
                return str(video_path), title, format_duration(duration)

            info = ydl.extract_info(url, download=True)
            path = Path(ydl.prepare_filename(info)).with_suffix(".opus")
            if path.exists():
                return str(path), title, format_duration(duration)

            return None, None, None
    except Exception:
        return None, None, None
