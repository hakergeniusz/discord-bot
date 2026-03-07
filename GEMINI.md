# GEMINI.md

## Project Overview
This project is a feature-rich, asynchronous Discord bot built using **Python 3.14+** and the **discord.py** library. It follows a modular architecture using "cogs" for command organization and a central `core` package for shared logic, configuration, and utilities.

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
- `src/main.py`: Entry point. Initializes the `MyBot` class (extending `commands.Bot`), sets up intents, and dynamically loads extensions from `src/cogs/`.
- `src/cogs/`: Contains modular command groups (extensions).
    - `admin.py`: Administrative commands (requires user ID in `config.yaml`).
    - `music.py`: Voice channel and music playback logic.
    - `fun.py`, `utility.py`, `other.py`: General purpose commands.
    - `error_handler.py`: Global error handling for commands.
- `src/core/`: Internal logic and utilities.
    - `config.py`: Loads environment variables (`.env`) and bot settings (`config.yaml`).
    - `admin_check.py`: Permission decorators for restricted commands.
    - `ai.py`: Integration with Google Gemini.
    - `youtube.py`: Music streaming logic using `yt-dlp`.
- `tests/`: Comprehensive test suite verifying core components and command syntax.

---

## Building and Running

### Prerequisites
- **OS:** Linux (Arch Linux/Debian 13 recommended; Windows/macOS not officially supported).
- **Tools:** `uv`, `git`, `FFmpeg`.

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
1.  **`.env`**: Store secrets here.
    ```env
    DISCORD_BOT_TOKEN=your_token
    GEMINI_API_KEY=your_gemini_key
    ```
2.  **`config.yaml`**: Store bot settings.
    ```yaml
    prefix: "!"
    admins:
      - 123456789  # Your Discord User ID
    ```

---

## Development Conventions

### Coding Style
- **PEP8 Compliance:** Enforced by `ruff`.
- **Type Hinting:** Required for all function signatures (as seen in `main.py` and `admin_check.py`).
- **Docstrings:** Use the **Google** convention.
- **Imports:** Sorted automatically by `ruff` (isort rules).

### Contribution Guidelines
- **Adding Commands:** Create a new file in `src/cogs/` or add to an existing one. Use `commands.Cog` and the `@commands.command()` or `@commands.hybrid_command()` decorators.
- **Permissions:** Use `@admin_check()` from `core.admin_check` for restricted commands.
- **Testing:** New features should include corresponding tests in the `tests/` directory.

### Project Specifics
- The bot targets **Python 3.14**, utilizing the latest language features.
- Dynamic Cog Loading: The bot automatically finds and loads all `.py` files in `src/cogs/` (excluding `__init__.py`).
- License: **GNU Affero General Public License v3 (AGPL-3.0)**.

### Note from a human
- If you see try-except without brackets in except, do not treat it as a bug. It is correct in Python 3.14 due to PEP 758 adding bracketless exceptions.
> Example
> ```python
> try:
>   # some code here
>   pass
> except discord.FirstException, discord.SecondException:
>   # a valid syntax!
>   pass
> ```