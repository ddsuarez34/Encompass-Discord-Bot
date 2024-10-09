# Commands

- !help: Help
- !play: Play or queue a song if one is already playing
- !queue: Print song queue
- !restart: Cleanup and disconnect bot from channels
- !skip: Next song
- !pause: Pause the current song
- !resume: Continue playing the paused song

# How to run

- Invite bot with admin rights to the server

## Docker container

- Install docker desktop
- Substitute DISCORD_TOKEN in .env file

Build the image in this folder

- `docker build -t discord-bot .`
  Run the image in docker desktop
  and test in discord server

## OR For Development

Requirements:

- Python 3.10
- ffmpeg executable (for audio processing)
- Discord Token (.env file)

Run `python main.py`

# TODO
- Limit !play song size / duration for safety
- Refactor using Cog design
- Add auto-disconnect when no more people are listening to the songs

