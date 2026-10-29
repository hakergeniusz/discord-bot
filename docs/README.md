# 🤖 Discord Bot

<img src="https://img.shields.io/badge/License-EUPL_v1.2-blue.svg?style=for-the-badge" height="40">
<img src="https://github.com/hakergeniusz/discord-bot/actions/workflows/tests.yml/badge.svg" height="40">

Yet Another Shitly Made Discord Bot — music, AI, Formula 1 and a healthy dose of nonsense.

---

## ✨ Features

| Area | Commands |
|---|---|
| 🎵 **Music** | `/play`, `/queue`, `/skip`, `/nowplaying`, `/leave` — YouTube playback powered by yt-dlp + FFmpeg |
| 🧠 **AI** | `/ai` — Google Gemini chat (free key from [AI Studio](https://aistudio.google.com)) |
| 🏎️ **Formula 1** | `/f1_standings`, `/f1_race_result`, `/f1_qualifying`, `/f1_calendar` |
| 🎉 **Fun** | `/cowsay`, `/archbtw`, `/complain`, `/finger`, `/heart`, `/howmanytimes`, `/howmanybutton`, `/nothing`, `/nvidia`, `/rickroll_me` |
| 🛠️ **Utility** | `/say`, `/webhook`, `/dm_or_not`, `/hide_conversation` |
| 👑 **Admin** | `/purge`, `/shutdown`, `/change_status`, `/create_webhook`, `/delete_webhook` — gated by the `admins` list in `config.yaml` |
| ℹ️ **Other** | `/ping`, `/source`, `/license` |

Errors are caught globally by a dedicated error handler cog, so a failing command won't crash the bot.

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
1. Download all files from this repository with `git clone https://github.com/hakergeniusz/discord-bot.git`.
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

---

## 🐳 Container

Every push to `main`/`latest` builds a multi-arch image (`linux/amd64`, `linux/arm64`, `linux/riscv64`) and publishes it to GHCR. Run it with:

```bash
docker run -d --name discord-bot \
  --env-file .env \
  -v ./config.yaml:/app/config.yaml:ro \
  ghcr.io/hakergeniusz/discord-bot:latest
```

The image runs the bot as an unprivileged user and reads its configuration from `/app/config.yaml` (mount yours as shown above); the `.env` values can equivalently be passed with `-e DISCORD_BOT_TOKEN=... -e GEMINI_API_KEY=...`.

---

## 🧪 Development

```bash
uv sync --all-extras --dev   # install runtime + dev dependencies
uv run pytest                # run the test suite
uv run ruff check .          # lint
uv run ruff format --check . # formatting check
```

Type checking is done with **basedpyright** in `standard` mode (see `pyproject.toml`).

---

## 🤖 CI

* **CI** (`.github/workflows/tests.yml`): Ruff lint + format check and the pytest suite on **Linux, Windows and macOS**.
* **Container** (`.github/workflows/container.yml`): podman builds for `amd64`/`arm64`/`riscv64` merged into a multi-arch manifest on GHCR.
* **Failure reporting**: when a push to `main` ends red, the workflows open (or update) an issue titled **🔴 CI failing on main** with a link to the failing run, and automatically close it once CI is green again.

---

## 🌟 Credits
All credits for are in [CREDITS](CREDITS) file.

---

## 📜 License

This software is licensed under the **European Union Public License (EUPL) version 1.2** or – as soon as they are approved by the European Commission – subsequent versions of the EUPL.

You may not use this work except in compliance with the Licence. You may obtain a copy of the Licence at:
[https://joinup.ec.europa.eu/software/page/eupl](https://joinup.ec.europa.eu/software/page/eupl)

Unless required by applicable law or agreed to in writing, software distributed under the Licence is distributed on an **"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND**, either express or implied. See the [LICENSE](LICENSE) file for the specific language governing permissions and limitations under the Licence.
