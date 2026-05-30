# 🤖 Discord Bot

<img src="https://img.shields.io/badge/License-EUPL_v1.2-blue.svg?style=for-the-badge" height="40">

---

## 👋 Introduction
Feature-rich Discord bot made by hakergeniusz with the goal of learning Discord.py.

---

## ⚙️ Prerequisites
You must have following installed on your computer for this bot to work correctly:
* A **Discord bot token** from Discord Developer Program.
*   **Linux, macOS, or Windows** operating system.
*   **Python 3.14**
*   **uv** for managing libraries
*   **Git** for cloning the repository
*   **FFmpeg** for `/play` command to work correctly (ensure it's in your PATH).

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

## 💻 System Compatibility
Bot is developed on **Arch Linux** and hosted on **Debian 13**. Bot is compatible with **Linux, Windows, and macOS**.
> **Note:** FFmpeg must be installed and added to the system's PATH for music features.

---

## 🌟 Credits
All credits for are in [CREDITS](CREDITS) file.

---

## 📜 License

This software is licensed under the **European Union Public License (EUPL) version 1.2** or – as soon as they are approved by the European Commission – subsequent versions of the EUPL.

You may not use this work except in compliance with the Licence. You may obtain a copy of the Licence at:
[https://joinup.ec.europa.eu/software/page/eupl](https://joinup.ec.europa.eu/software/page/eupl)

Unless required by applicable law or agreed to in writing, software distributed under the Licence is distributed on an **"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND**, either express or implied. See the [LICENSE](LICENSE) file for the specific language governing permissions and limitations under the Licence.