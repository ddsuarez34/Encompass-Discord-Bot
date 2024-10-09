from dotenv import load_dotenv
import os

load_dotenv()

# config.py
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

CHANNEL_ID = os.getenv('CHANNEL_ID', 1293115193357766700)
FFMPEG_PATH = os.getenv('FFMPEG_PATH', "/usr/bin/ffmpeg")


YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'quiet': True
}


FFMPEG_OPTIONS = {
    'before_options': '-loglevel verbose -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -ar 48000 -b:a 192k'
}
