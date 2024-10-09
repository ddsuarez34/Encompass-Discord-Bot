import asyncio
from collections import deque
import random
import re
import logging
import discord
import discord.context_managers
from discord.ext import commands

from config import CHANNEL_ID, DISCORD_TOKEN, FFMPEG_OPTIONS
from config import FFMPEG_PATH as ffmpeg_path
from helper import extract_info

logger = logging.getLogger()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

song_queue = deque()
is_playing = False

@bot.event
async def on_ready():
    welcome_messages = ["Buenas tardes jovenes"]
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(random.choice(welcome_messages))


@bot.command(help="Plays a song, interrupts a song if one is playing. Format: !play <URL / song name>")
async def play(ctx, *, args: str = commands.parameter(default=None, description=": Song name or Youtube URL")):
    logger.debug("!play command")
    global is_playing
    global song_queue

    if args is None:
        await ctx.send("Enter something...!!!")
        return

    # Checks if the user is in a VC
    if ctx.author.voice is None:
        await ctx.send("You're not in a voice channel.")
        return

    channel = ctx.author.voice.channel
    # If the bot is not connected to a voice channel, connect it to the user's channel
    if ctx.voice_client is None:
        await channel.connect()
        await asyncio.sleep(1)  
    elif (
        ctx.voice_client.channel != channel
    ):  # If bot is in another channel, move it to the user's channel
        await ctx.voice_client.move_to(channel)
        await asyncio.sleep(1)

    loop = asyncio.get_event_loop()
    if re.match(r"^https?://(?:www\.)?youtube\.com/watch\?v=", args):
        # Get direct URL
        info = await loop.run_in_executor(
            None, extract_info, args
        )  # Run in a separate thread
    else:
        info = await loop.run_in_executor(None, extract_info, args, True)
        info = info["entries"][0]

    song = dict()
    song['title'] = info['title']
    song['url'] = info['url']
    logger.debug(song)
    # Play the audio in the voice channel
    # If nothing is currently playing, start playing the song immediately
    song_queue.append(song)
    if not is_playing:
        await play_next(ctx)
    else:
        await ctx.send(f"Added to queue: {song['title']}")


# Function to play the next song in the queue
async def play_next(ctx):
    logger.debug(f"Voice client status before playing: is_playing={ctx.voice_client.is_playing()}, is_paused={ctx.voice_client.is_paused()}")
    global is_playing
    global song_queue

    if ctx.voice_client.is_playing():
        logger.debug("Already playing audio, stopping it first.")
        ctx.voice_client.stop()

    if len(song_queue) > 0:
        is_playing= True
        song = song_queue.popleft()  # Get the next song from the queue
        with open('ffmpeg_error.log', 'w') as ffmpeg_stderr:
            try:
                ctx.voice_client.play(
                    discord.FFmpegPCMAudio(song['url'], executable=ffmpeg_path, **FFMPEG_OPTIONS, stderr=ffmpeg_stderr),
                    after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop), 
                )
                await ctx.send(f"Now playing: {song['title']}")
            except Exception as e:
                logger.error(f"Failed to play song: {e}")
                await ctx.send(f"Error playing song: {e}")
                is_playing = False
    else:
        is_playing = False
        await ctx.send("Queue is empty, nothing to play next.")

# Command to skip the current song
@bot.command(help="Skips the currently playing song.")
async def skip(ctx):
    if ctx.voice_client is not None and ctx.voice_client.is_playing():
        ctx.voice_client.stop()  # This triggers the `after` function in play

# Command to show the current queue
@bot.command(help="Displays the current song queue.")
async def queue(ctx):
    if len(song_queue) == 0:
        await ctx.send("The queue is currently empty.")
    else:
        queue_list = '\n'.join([f"{i + 1}. {song['title']}" for i, song in enumerate(song_queue)])
        await ctx.send(f"Current queue:\n{queue_list}")

@bot.command(help="Pauses the currently playing song.")
async def pause(ctx):
    # Check if the bot is playing something
    if ctx.voice_client is not None and ctx.voice_client.is_playing():
        ctx.voice_client.pause()  # Pauses the current song
        await ctx.send("Paused the song.")
    else:
        await ctx.send("There is no song currently playing.")

@bot.command(help="Resumes the paused song.")
async def resume(ctx):
    # Check if the bot is paused
    if ctx.voice_client is not None and ctx.voice_client.is_paused():
        ctx.voice_client.resume()  # Resumes the song
        await ctx.send("Resumed the song.")
    else:
        await ctx.send("There is no paused song to resume.")

# Restart the bot
@bot.command(help="Restarts the bot (Flush queue and stop playing all music)")
async def restart(ctx):
    logger.info("Restarting bot...")
    logger.debug(f'Voice client before cleanup is None?: {ctx.voice_client == None}')

    global is_playing
    global song_queue

    # Clear the song queue and stop playback
    song_queue.clear()
    is_playing = False
    if ctx.voice_client is not None:
        ctx.voice_client.stop()
        await asyncio.sleep(1)  
        ctx.voice_client.cleanup()
        await ctx.voice_client.disconnect()

# Run the bot
bot.run(DISCORD_TOKEN, root_logger=True)
