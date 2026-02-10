# 🤖 Discord Bot

<img src="https://img.shields.io/badge/License-AGPLv3-orange.svg?style=for-the-badge" height="40">

---

## 👋 Introduction
Feature-rich Discord bot made by hakergeniusz with the goal of learning Discord.py. It is licenced with GNU Affero General Public License version 3.

---

## ⚙️ Prerequisites
You must have following installed on your computer for this bot to work correctly:
* A **Discord bot token** from Discord Developer Program.
* A **Linux** operating system. **Code will not work on Windows**
* **Python 3.14**
* **uv** for managing libraries
* **Git** for cloning the repository
* **FFmpeg** for `/play` command to work correctly.

---

## 💻 Preparation
1. Download all files from this repository with `git clone -b main https://github.com/hakergeniusz/discord-bot.git`.
> NOTE: If you want `latest` branch with new features (also broken bot), use `git clone -b latest https://github.com/hakergeniusz/discord-bot.git`.
2. Open the folder with `cd discord-bot`.
3. Create and fill up `.env` and `config.yaml` file.
4. Run `uv sync` to install all required libraries.

> **`.env` values:**
> ```
> DISCORD_BOT_TOKEN=YOUR_BOT_TOKEN
> GEMINI_API_KEY=GOOGLE_AI_STUDIO_KEY
> ```
> * `DISCORD_BOT_TOKEN`: Your Discord bot token from Discord Developer Program.
> * `GEMINI_API_KEY`: Your Google AI Studio API key (obtainable for free on aistudio.google.com).

> **Example `config.yaml` file:**
> ```
> prefix: "!"
> admins:
>    - 123456789
>    - 987654321
> ```
> * `prefix`: The prefix for bot commands. Default is `!`
> * `admins`: List for Discord user IDs that have access to admin commands.


---

## 🚀 Running the bot
Execute the following command:
```bash
uv run bot
```

## 🐧 System Compatibility
Bot is actively developed on **Arch Linux** and hosted on **Debian 13**. Bot should work on most Linux distributions.
> **Note:** No support or instructions will be provided for Windows or macOS (macOS may work due to UNIX compatibility).

---

## 🌟 Credits
All credits for are in [CREDITS](CREDITS) file.

---

## 📜 License

This program is free software: you can redistribute it and/or modify it under the terms of the **GNU Affero General Public License** as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of **MERCHANTABILITY** or **FITNESS FOR A PARTICULAR PURPOSE**. See the [LICENSE](LICENSE) file for more details.
