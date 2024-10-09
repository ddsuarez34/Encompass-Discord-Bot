from dotenv import load_dotenv
import os

load_dotenv()

# config.py
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

CHANNEL_ID = 1293115193357766700
FFMPEG_PATH = "C:/ffmpeg/bin/ffmpeg.exe"


YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True
}


FFMPEG_OPTIONS = {
    'before_options': '-loglevel verbose -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}
