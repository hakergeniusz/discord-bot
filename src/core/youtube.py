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
