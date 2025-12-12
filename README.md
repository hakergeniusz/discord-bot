# 🤖 Discord Bot

## 👋 Introduction
This bot has been made by me with goal to learning Discord.py, it may not be useful on your Discord server. You are free to use my code in your Discord.py bot without asking me for permission.


## ⚙️ Prerequisites
You must have following installed on your computer for this bot to work correctly:
* A **Discord bot token** from Discord Developer Program.
* **Python 3.10+**
* **Ollama** installed on your system with the following language models:
  * `gemma3:270m`
  * `llama-guard3:1b`
* **Git** for cloning the repository.
* **FFmpeg** for `/play` command to work correctly.
* **`example.mp3`** file for the `/play` command to get a file to play. If you don't have one, you can use the default one that is in the repository.


## 💻 Preparation
NOTE: These commands are for Linux. If you use Windows, please use **Windows Subsystem for Linux** (WSL).
1. Download all files from this repository with `git clone https://github.com/hakergeniusz/discord-bot.git`.
2. Open the folder with `cd discord-bot`.
3. Create a Python Venv with `python3 -m venv .venv`.
4. Activate Venv with `source .venv/bin/activate`.
5. Install all required libraries with `pip install -r requirements.txt`.
6. Fill up `.env` file.

> **Note on `.env` values:**
> ```
> DISCORD_BOT_TOKEN=YOUR_BOT_TOKEN
> OWNER_ID=YOUR_DISCORD_ID
> ```
> * `DISCORD_BOT_TOKEN`: Your Discord bot token from Discord Developer Program.
> * `OWNER_ID`: Your Discord user ID or other account that you want it to have all permissions


## 🚀 Running the bot
With your `.venv` active, execute the following command: 
```bash
python3 bot.py
```
