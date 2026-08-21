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

"""Module for utility functions to download and process YouTube videos."""

import json
import re
from pathlib import Path

import yt_dlp

from core.config import SECONDS_IN_MINUTE, TMP_BASE

CACHE_DIR = TMP_BASE
URL_REGEX = (
    r"(https?://)?(www\.|m\.)?"
    r"(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/)"
    r"([\w-]{11})"
)

YDL_OPTS = {
    "outtmpl": str(CACHE_DIR / "%(id)s.%(ext)s"),
    "format": "bestaudio/best",
    "noplaylist": True,
    "writethumbnail": True,
    "quiet": True,
    "no_warnings": False,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "source_address": "0.0.0.0",  # noqa: S104
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "opus",
            "preferredquality": "192",
        },
    ],
}


def get_yt_video_id(url: str) -> str | None:
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
    if seconds < SECONDS_IN_MINUTE:
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


def _process_video_info(
    info: dict,
    video_id: str,
    video_path: str,
    metadata_path: str,
) -> tuple[str | None, str | None, str | None, str | None, str | None] | None:
    """Process video info and save metadata.

    Args:
        info: Video info from yt-dlp.
        video_id: The video ID.
        video_path: Path to the video file.
        metadata_path: Path to the metadata file.

    Returns:
        Tuple of video info or None if processing failed.
    """
    if not info:
        return None

    title = info.get("title")
    duration = info.get("duration")
    video_id = info.get("id")
    thumbnail = info.get("thumbnail")
    formatted_duration = format_duration(int(duration)) if duration else "0 seconds"

    metadata = {
        "title": title,
        "duration": formatted_duration,
        "thumbnail": thumbnail,
    }
    with Path(metadata_path).open("w", encoding="utf-8") as f:
        json.dump(metadata, f)

    if Path(video_path).exists():
        return (str(video_path), title, formatted_duration, thumbnail, video_id)

    return None


def download_youtube_video(
    url: str,
) -> tuple[str | None, str | None, str | None, str | None, str | None]:
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
    """
    match = re.search(URL_REGEX, url)
    video_id = match.group(match.lastindex or 0) if match else None
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
        except json.JSONDecodeError, OSError:
            pass

    try:
        return _download_and_process(url, video_id, video_path, metadata_path)
    except yt_dlp.DownloadError, OSError, TypeError:
        return None, None, None, None, None


def _download_and_process(
    url: str,
    video_id: str,
    video_path: Path,
    metadata_path: Path,
) -> tuple[str | None, str | None, str | None, str | None, str | None]:
    """Download and process video info.

    Args:
        url: The YouTube URL.
        video_id: The video ID.
        video_path: Path to the video file.
        metadata_path: Path to the metadata file.

    Returns:
        Tuple of video info or None if processing failed.
    """
    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        if video_path.exists():
            info = ydl.extract_info(url, download=False)
        else:
            info = ydl.extract_info(url, download=True)

        result = _process_video_info(
            info,
            video_id,
            str(video_path),
            str(metadata_path),
        )
        if result is not None:
            return result

        return None, None, None, None, None
