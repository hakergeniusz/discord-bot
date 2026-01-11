import yt_dlp
import re
import os

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