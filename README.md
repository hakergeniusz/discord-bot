# 🤖 Discord Bot
<img src="https://cdn.jsdelivr.net/npm/@intergrav/devins-badges@3/assets/cozy/unsupported/risugamis-modloader_vector.svg" height="60">

<img src="https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge" height="60">

## 👋 Introduction
This bot has been made by me with goal to learning Discord.py, it may not be useful on your Discord server.

## ⚙️ Prerequisites
You must have following installed on your computer for this bot to work correctly:
* A **Discord bot token** from Discord Developer Program.
* **Python 3.10+**
* **Ollama** installed on your system with the following language models:
  * `gemma3:1b`
  * `gemma3:4b`
  * `qwen2.5-coder:7b`
> If you don't want to install all of these models, remove `gemma3:4b` and `qwen2.5-coder:7b` from menu selection from `/ai` . These two lines are highlighted with a comment.
* **Git** for cloning the repository.
* **FFmpeg** for `/play` command to work correctly.
* **`example.mp3`** file for the `/play` command to get a file to play. If you don't have one, you can use the default one that is in the repository.


## 💻 Preparation
NOTE: These commands are for Linux. If you use Windows, please use **Windows Subsystem for Linux** (WSL).
1. Download all files from this repository with `git clone https://github.com/hakergeniusz/discord-bot.git`.
> **Note:** When downloading by this exact command, you download from `main` branch. Main branch may have unfinished changes. However though, `main` branch receives bug fixes before they are released.
2. Open the folder with `cd discord-bot`.
3. Create a Python venv with `python3 -m venv .venv`.
4. Activate venv with `source .venv/bin/activate`.
5. Install all required libraries with `pip install -r requirements.txt`.
6. Create and fill up `.env` file.

> **Note on `.env` values:**
> ```
> DISCORD_BOT_TOKEN=YOUR_BOT_TOKEN
> DISCORD_OWNER_ID=YOUR_DISCORD_ID
> ```
> * `DISCORD_BOT_TOKEN`: Your Discord bot token from Discord Developer Program.
> * `DISCORD_OWNER_ID`: Your Discord user ID or other account that you want it to have all permissions


## 🚀 Running the bot
With your `.venv` active, execute the following command:
```bash
python3 bot.py
```
