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

"""Unit tests for the YouTube core module."""

from unittest.mock import MagicMock, patch

from src.core.youtube import CACHE_DIR, download_youtube_video, get_yt_video_id


def test_get_yt_video_id() -> None:
    """Test YouTube video ID extraction."""
    url = "https://www.youtube.com/watch?v=NonExisting"
    assert get_yt_video_id(url) == "NonExisting"


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
