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

"""Module for utility functions to download and process YouTube videos."""

import json
import re
from pathlib import Path
from typing import Optional

import yt_dlp

CACHE_DIR = Path("/tmp")
URL_REGEX = (
    r"(https?://)?(www\.|m\.)?"
    r"(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)"
    r"([\w-]{11})"
)

ydl_opts = {
    "outtmpl": "/tmp/%(id)s.%(ext)s",
    "format": "bestaudio/best",
    "noplaylist": True,
    "writethumbnail": True,
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
) -> tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]:
    """Downloads a YouTube video and extracts metadata.

    This function attempts to download a video in .opus format using yt-dlp.
    It implements a caching mechanism: if the file and its metadata already exist
    in CACHE_DIR, it returns the cached data instead of downloading again.

    Args:
        url (str): The full YouTube video URL to process.

    Returns:
        tuple: A five-element tuple containing:
            - path (str | None): Absolute path to the downloaded .opus file.
            - title (str | None): The title of the video.
            - duration (str | None): Formatted duration (e.g., "4 minutes 20 seconds").
            - thumbnail (str | None): Direct URL to the video's thumbnail image.
            - video_id (str | None): The extracted YouTube video ID.

            Returns (None, None, None, None, None) if the URL is invalid,
            the download fails, or metadata cannot be processed.
    """  # noqa: E501
    match = re.search(URL_REGEX, url)
    if not match:
        return None, None, None, None, None

    video_id = match.group(match.lastindex or 0)
    if not isinstance(video_id, str):
        return None, None, None, None, None
    video_path = CACHE_DIR / f"{video_id}.opus"
    metadata_path = CACHE_DIR / f"{video_id}.metadata.json"

    if video_path.exists() and metadata_path.exists():
        try:
            with metadata_path.open("r", encoding="utf-8") as f:
                metadata = json.load(f)
                return (
                    str(video_path),
                    metadata.get("title"),
                    metadata.get("duration"),
                    metadata.get("thumbnail"),
                    video_id,
                )
        except (json.JSONDecodeError, OSError):
            pass

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if video_path.exists():
                info = ydl.extract_info(url, download=False)
            else:
                info = ydl.extract_info(url, download=True)

            if not info:
                return None, None, None, None, None

            video_id = info.get("id")
            title = info.get("title")
            duration = info.get("duration")
            video_id = info.get("id")
            thumbnail = info.get("thumbnail")
            formatted_duration = (
                format_duration(int(duration)) if duration else "0 seconds"
            )

            metadata = {
                "title": title,
                "duration": formatted_duration,
                "thumbnail": thumbnail,
            }
            with metadata_path.open("w", encoding="utf-8") as f:
                json.dump(metadata, f)

            if video_path.exists():
                return (str(video_path), title, formatted_duration, thumbnail, video_id)

            return None, None, None, None, None
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None, None, None, None, None
