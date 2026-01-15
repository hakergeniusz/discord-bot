import pytest
from unittest.mock import patch, MagicMock
from src.core.youtube import download_youtube_video, get_yt_video_id
import os

def test_get_yt_video_id():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert get_yt_video_id(url) == "dQw4w9WgXcQ"

def test_download_youtube_video_cached():
    video_id = "dQw4w9WgXcQ"
    url = f"https://www.youtube.com/watch?v={video_id}"
    cache_path = f"/tmp/{video_id}.opus"
    
    with patch("os.path.exists") as mock_exists:
        mock_exists.side_effect = lambda p: p == cache_path or p == "/tmp/" 
        def side_effect(path):
            if path == cache_path: return True
            return False
            
        mock_exists.side_effect = side_effect
        
        result = download_youtube_video(url)
        assert result == cache_path

@patch("yt_dlp.YoutubeDL")
def test_download_youtube_video_failure(mock_ydl):
    instance = mock_ydl.return_value.__enter__.return_value
    instance.extract_info.side_effect = Exception("Download failed")
    
    url = "https://www.youtube.com/watch?v=invalid"
    result = download_youtube_video(url)
    assert result is None
