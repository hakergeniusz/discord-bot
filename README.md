## Introduction
This bot has been made to learn Discord.py and it is not useful on a server. 

## Prerequisites
You must have following installed on your computer for this bot to work correctly:
* A **Discord bot token** from Discord Developer Program.
* **Python 3.10+**
* **Ollama** installed on your system with the following language models:
  * `gemma3:270m`
  * `llama-guard3:1b`
* **Git** for cloning the repository.

## Preparation
NOTE: These commands are for Linux. If you use Windows, please use **Windows Subsystem for Linux** (WSL).
1. Download all files from this repository with `git clone https://github.com/hakergeniusz/discord-bot.git`.
2. Open the folder with `cd discord-bot`.
3. Create a Python Venv with `python3 -m venv .venv`.
4. Activate Venv with `source .venv/bin/activate`.
5. Install all required libraries with `pip install -r requirements.txt`.
6. Install my library from `libr.zip`.
7. Fill up `.env` file.


> **Note on `.env` values:**
> ```
> DISCORD_BOT_TOKEN=YOUR_BOT_TOKEN
> OWNER_ID=YOUR_DISCORD_ID
> ```
> * `DISCORD_BOT_TOKEN`: Your Discord bot token from Discord Developer Program.
> * `OWNER_ID`: Your Discord user ID or other account that you want it to have all permissions

## Running the bot
With `.venv` open, execute the following command: 
```bash
python3 bot.py
```
