import yt_dlp as youtube_dlp
from config import YDL_OPTIONS


def extract_info(query, search=False):
    with youtube_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        if search:
            # Use YouTube search to get the first result
            query = f"ytsearch:{query}"  # yt-dlp format for searching YouTube
        return ydl.extract_info(query, download=False)  # Return search result or video info