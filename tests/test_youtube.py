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

from unittest.mock import MagicMock, patch

from src.core.youtube import download_youtube_video, get_yt_video_id


def test_get_yt_video_id() -> None:
    """Test YouTube video ID extraction."""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert get_yt_video_id(url) == "dQw4w9WgXcQ"


@patch("src.core.youtube.Path.exists")
@patch("yt_dlp.YoutubeDL")
def test_download_youtube_video_cached(
    mock_ydl: MagicMock, mock_exists: MagicMock
) -> None:
    """Test downloading a video that is already cached."""
    video_id = "dQw4w9WgXcQ"
    url = f"https://www.youtube.com/watch?v={video_id}"
    cache_path = f"/tmp/{video_id}.opus"

    instance = mock_ydl.return_value.__enter__.return_value
    instance.extract_info.return_value = {
        "id": video_id,
        "title": "Test Title",
        "duration": 60,
        "thumbnail": "https://example.com/thumb.jpg",
    }

    mock_exists.return_value = True

    path, title, duration, thumbnail, video_id = download_youtube_video(url)
    assert path == cache_path
    assert title == "Test Title"
    assert duration == "1 minute"
    assert thumbnail == "https://example.com/thumb.jpg"


@patch("yt_dlp.YoutubeDL")
def test_download_youtube_video_failure(mock_ydl: MagicMock) -> None:
    """Test video download failure."""
    instance = mock_ydl.return_value.__enter__.return_value
    instance.extract_info.side_effect = Exception("Download failed")

    url = "https://www.youtube.com/watch?v=invalid"
    result = download_youtube_video(url)
    assert result == (None, None, None, None, None)
