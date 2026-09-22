# Copyright (c) 2025-present hakergeniusz
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

"""Unit tests for the YouTube core module."""

from typing import TYPE_CHECKING
from unittest.mock import MagicMock, patch

from src.core.youtube import (
    CACHE_DIR,
    _process_video_info,
    download_youtube_video,
    format_duration,
    get_yt_video_id,
)

if TYPE_CHECKING:
    from pathlib import Path


def test_get_yt_video_id() -> None:
    """Test YouTube video ID extraction."""
    url = "https://www.youtube.com/watch?v=NonExisting"
    assert get_yt_video_id(url) == "NonExisting"


def test_get_yt_video_id_not_youtube() -> None:
    """Test YouTube video ID extraction for invalid link."""
    url = "https://www.discord.com/robots.txt"
    assert not get_yt_video_id(url)


@patch("src.core.youtube.yt_dlp.YoutubeDL")
def test_download_youtube_video_cached(
    mock_ydl: MagicMock,
) -> None:
    """Test downloading a video that is already cached."""
    video_id = "NonExisting"
    url = f"https://www.youtube.com/watch?v={video_id}"
    cache_path = str(CACHE_DIR / f"{video_id}.opus")

    instance = mock_ydl.return_value.__enter__.return_value
    instance.extract_info.return_value = {
        "id": video_id,
        "title": "Test Title",
        "duration": 60,
        "thumbnail": "https://example.com/thumb.jpg",
    }

    with (
        patch("src.core.youtube.json.load") as mock_json_load,
        patch("src.core.youtube.open", create=True),
        patch("src.core.config.Path.exists", return_value=True),
    ):
        mock_json_load.return_value = {
            "title": "Test Title",
            "duration": "1 minute",
            "thumbnail": "https://example.com/thumb.jpg",
        }
        path, title, duration, thumbnail, video_id_out = download_youtube_video(url)
        assert path == cache_path
        assert title == "Test Title"
        assert duration == "1 minute"
        assert thumbnail == "https://example.com/thumb.jpg"
        assert video_id_out == video_id


@patch("yt_dlp.YoutubeDL")
def test_download_youtube_video_failure(mock_ydl: MagicMock) -> None:
    """Test video download failure."""
    instance = mock_ydl.return_value.__enter__.return_value
    instance.extract_info.side_effect = Exception("Download failed")

    url = "https://www.youtube.com/watch?v=invalid"
    result = download_youtube_video(url)
    assert result == (None, None, None, None, None)


def test_format_duration_only_seconds() -> None:
    """Test time formatting with input lower than 60."""
    assert format_duration(45) == "45 seconds"


def test_format_duration_only_minutes() -> None:
    """Test time formatting with input of more than 60, with multiply of 60."""
    assert format_duration(120) == "2 minutes"


def test_format_duration_with_minutes() -> None:
    """Test time formatting with input of more than 60."""
    assert format_duration(100) == "1 minute 40 seconds"


def test_format_duration_only_hours() -> None:
    """Test time formatting with input of more than 3600, with multiply of 3600."""
    assert format_duration(7200) == "2 hours"


def test_format_duration_with_hours() -> None:
    """Test time formatting with input of more than 3600."""
    assert format_duration(7321) == "2 hours 2 minutes 1 second"


def test_process_video_info_no_info() -> None:
    """Test processing video information without info."""
    assert (
        _process_video_info(
            info=None,
            video_id="dummy",
            video_path="dummy",
            metadata_path="dummy",
        )
        is None
    )


def test_process_video_info(tmp_path: Path) -> None:
    """Test processing video information."""
    info = {
        "id": "dQw4w9WgXcQ",
        "title": "Never Gonna Give You Up",
        "duration": 212,
        "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
    }
    video_path = str(tmp_path / "v.opus")
    metadata_path = str(tmp_path / "test.json")
    (tmp_path / "v.opus").touch()
    should_output = (
        str(video_path),
        "Never Gonna Give You Up",
        "3 minutes 32 seconds",
        "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
        "dQw4w9WgXcQ",
    )
    assert (
        _process_video_info(
            info=info,
            video_id="dQw4w9WgXcQ",
            video_path=video_path,
            metadata_path=metadata_path,
        )
        == should_output
    )


def test_process_video_info_no_video_in_path(tmp_path: Path) -> None:
    """Test processing video information with invalid video path."""
    info = {
        "id": "dQw4w9WgXcQ",
        "title": "Never Gonna Give You Up",
        "duration": 212,
        "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
    }
    video_path = str(tmp_path / "v.opus")
    metadata_path = str(tmp_path / "test.json")
    assert (
        _process_video_info(
            info=info,
            video_id="dQw4w9WgXcQ",
            video_path=video_path,
            metadata_path=metadata_path,
        )
        is None
    )


def test_video_download_good_json(tmp_path: Path) -> None:
    """Test cached download with valid metadata JSON."""
    with patch("src.core.youtube.CACHE_DIR", tmp_path):
        (tmp_path / "dQw4w9WgXcQ.opus").touch()
        contents = """
        {
            "title": "Never Gonna Give You Up",
            "duration": "3 minutes 32 seconds",
            "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg"
        }
        """
        (tmp_path / "dQw4w9WgXcQ.metadata.json").write_text(contents, encoding="utf-8")
        result = download_youtube_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        assert result == (
            str(tmp_path / "dQw4w9WgXcQ.opus"),
            "Never Gonna Give You Up",
            "3 minutes 32 seconds",
            "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
            "dQw4w9WgXcQ",
        )
