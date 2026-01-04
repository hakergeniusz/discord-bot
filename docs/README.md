# 🤖 Discord Bot

<img src="https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge" height="60">

---

## 👋 Introduction
Feature-rich Discord bot made by hakergeniusz with the goal of learning Discord.py. It is licenced with GNU General Public License version 3.

---

## ⚙️ Prerequisites
You must have following installed on your computer for this bot to work correctly:
* A **Discord bot token** from Discord Developer Program.
* **Python 3.12+**
* **Git** for cloning the repository.
* **FFmpeg** for `/play` command to work correctly.
* **`example.mp3`** file for the `/play` command to get a file to play. If you don't have one, you can use the default one that is in the repository.
* **beep** linux package for `/beep`.

---

## 💻 Preparation
NOTE: These commands are for Linux. If you use Windows, please use **Windows Subsystem for Linux** (WSL).
1. Download all files from this repository with `git clone -b main https://github.com/hakergeniusz/discord-bot.git`.
> NOTE: If you want `latest` branch with new features (also broken bot), use `git clone -b latest https://github.com/hakergeniusz/discord-bot.git`.
2. Open the folder with `cd discord-bot`.
3. Create a Python venv with `python3 -m venv .venv`.
4. Activate venv with `source .venv/bin/activate`.
5. Install all required libraries with `pip install -r requirements.txt`.
6. Create and fill up `.env` file.

> **Note on `.env` values:**
> ```
> DISCORD_BOT_TOKEN=YOUR_BOT_TOKEN
> DISCORD_OWNER_ID=YOUR_DISCORD_ID
> POWEROFF_COMMAND=True/False
> ```
> * `DISCORD_BOT_TOKEN`: Your Discord bot token from Discord Developer Program.
> * `DISCORD_OWNER_ID`: Your Discord user ID or other account that you want it to have all permissions.
> * `POWEROFF_COMMAND`: `True` if you want `/turn_off_pc` to work, anything else if you don't want it to work. If value is not provided, it is default set to `False`.

---

## 🚀 Running the bot
With your `.venv` active, execute the following command:
```bash
python3 main.py
```

---

## 🎵 Credits
The `example.mp3` used for the music features is provided by **NoCopyrightSounds**:
* **Song:** Cartoon, Jéja - On & On (feat. Daniel Levi) [NCS Release]
* **Video:** https://www.youtube.com/watch?v=K4DyBUG242c
* **Free Download / Stream:** https://ncs.io/OnandOn

All credits for Python libraries are in [CREDITS](CREDITS) file.

---

## 📜 License
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of **MERCHANTABILITY** or **FITNESS FOR A PARTICULAR PURPOSE**. See the [COPYING](COPYING) file for more details.