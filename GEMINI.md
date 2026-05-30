# GEMINI.md

## Project Overview
This project is a feature-rich, asynchronous Discord bot built using **Python 3.14+** and the **discord.py** library.

### Main Technologies
- **Language:** Python 3.14+
- **Library:** `discord.py` (v2.6.4+)
- **Dependency Manager:** `uv`
- **AI Integration:** `google-genai` (Gemini API)
- **Media:** `yt-dlp` (YouTube/Music support), `FFmpeg` (required for voice)
- **Configuration:** `pyyaml` (YAML), `python-dotenv` (ENV)
- **Linting/Formatting:** `ruff` (Strict PEP8, Google docstring convention)
- **Testing:** `pytest`, `pytest-asyncio`

### Architecture
- `src/main.py`: Entry point. Initializes the bot.
- `src/cogs/`: Contains modular command groups (extensions).
- `src/core/`: Internal logic and utilities (configuration, AI integration, admin checks).
- `tests/`: Comprehensive test suite.

---

## Building and Running

### Prerequisites
- **OS:** Linux (Arch Linux/Debian 13 recommended).
- **Tools:** `uv`, `git`, `FFmpeg`, `Python 3.14+`.

### Commands
- **Install Dependencies:**
  ```bash
  uv sync
  ```
- **Run the Bot:**
  ```bash
  uv run bot
  ```
- **Run Tests:**
  ```bash
  pytest
  ```
- **Linting:**
  ```bash
  ruff check .
  ```

### Configuration
1.  **`.env`**: Store secrets.
    ```env
    DISCORD_BOT_TOKEN=your_token
    GEMINI_API_KEY=your_gemini_key
    ```
2.  **`config.yaml`**: Store bot settings.
    ```yaml
    prefix: "!"
    admins:
      - 123456789  # Discord User ID
    ```

---

## Development Conventions

### Coding Style
- **PEP8 Compliance:** Enforced by `ruff`.
- **Type Hinting:** Required for function signatures.
- **Docstrings:** Use the **Google** convention.

### License
This software is licensed under the **European Union Public License (EUPL) version 1.2**.
