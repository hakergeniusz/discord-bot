# GEMINI.md - Discord Bot Project Guide

This document provides foundational mandates, architectural patterns, and development workflows for AI agents working on the `discord-bot` project.

## 1. Project Overview
- **Name:** discord-bot
- **Description:** A modern, feature-rich Discord bot built with `discord.py`.
- **Version:** 2.1.0
- **License:** EUPL-1.2 (European Union Public Licence) - **Copyright header is MANDATORY on every file.**
- **Tech Stack:**
  - **Language:** Python 3.14+ (Strict typing, modern features).
  - **Framework:** `discord.py` (version >= 2.6.4).
  - **AI Integration:** Google GenAI (`google-genai`) using Gemma 4 models.
  - **Music:** `yt-dlp` and `FFmpeg`.
  - **Tooling:** `uv` (Package management), `ruff` (Linting/Formatting), `pytest` (Testing).

## 2. Core Architecture

The project follows a modular "Cogs & Core" architecture:

### `src/main.py`
- The entry point of the application.
- Uses a custom `MyBot(commands.Bot)` class.
- Implements an automatic cog loader that walks through `src/cogs/` and loads all `.py` files.
- Configures `asyncio` event loop policies (e.g., `WindowsProactorEventLoopPolicy` on Windows).

### `src/cogs/` (Interface Layer)
- Contains Discord-specific logic (commands, event listeners).
- **Key Components:**
  - `on_startup.py`: Contains `SyncCog` for tree synchronization (`bot.tree.sync()`) and status management.
  - `error_handler.py`: Global error handling for both prefix and slash commands.
- **Conventions:**
  - Use `commands.hybrid_command` whenever possible to support both prefix and slash commands.
  - Use `app_commands.describe` for parameter documentation.
  - Use `ctx.defer()` for commands that take more than 3 seconds to process.
  - Organized by domain: `admin.py`, `music.py`, `fun.py`, `utility.py`, etc.

### `src/core/` (Logic Layer)
- Contains pure Python logic, API wrappers, and utilities.
- Should remain decoupled from Discord-specific objects (like `Context` or `Message`) where possible.
- **Key Modules:**
  - `ai.py`: Interface with Google's Gemma models.
  - `config.py`: Centralized configuration and constants.
  - `logger.py`: Standardized logging setup.
  - `admin_check.py`: Custom decorators for permission management.
  - `f1.py`, `youtube.py`, `image_checker.py`: Specialized domain logic.

## 3. Engineering Standards

### Coding Style
- **Linting:** `ruff` is used with the `ALL` rule set (with minor exceptions in `pyproject.toml`).
- **Formatting:** Handled by `ruff`. Line length limit: 100 characters.
- **Type Safety:** Strict type hints are required for all function signatures and complex variables. Use `TYPE_CHECKING` for circular imports.
- **Docstrings:** Use **Google Style** docstrings. Required for all classes and public methods.

### File Headers
Every Python file MUST begin with the following copyright and license header:
```python
# Copyright (c) 2025-2026 hakergeniusz
#
# Licensed under the EUPL, Version 1.2 or - as soon they will be approved by the European
# Commission - subsequent versions of the EUPL (the "Licence"); You may not use this work
# except in compliance with the Licence.
# ... (rest of the license block)
```

### Error Handling
- Use `src/cogs/error_handler.py` for global command error handling.
- Inside logic, prefer specific exceptions and logging via `core.logger`.
- Avoid "silent" failures; always inform the user or log the error.

## 4. Development Workflows

### Environment Setup
- Use `uv` for dependency management: `uv sync`.
- Secrets are managed via `.env` (refer to `src/core/config.py` for required keys).
- Global settings are in `config.yaml`.

### Testing
- **Framework:** `pytest` with `pytest-asyncio`.
- **Location:** `tests/` directory.
- **Convention:** Every new feature or bug fix must include corresponding tests.
- **Running Tests:** `pytest`.

### Adding a New Command
1. If it's a new category, create a new cog in `src/cogs/`.
2. Implement the command as a `hybrid_command`.
3. Move any heavy processing or external API calls to a new or existing module in `src/core/`.
4. Add permission checks using `@admin_check()` if needed.
5. Update `tests/` to cover the new functionality.

## 5. Deployment & CI
- **GitHub Actions:** `.github/workflows/tests.yml` runs tests on every push.
- **Version Management:** Follow semantic versioning in `pyproject.toml`.

## 6. Project Quirks & Important Notes
- **Python 3.14:** Ensure you are using features compatible with this version or later.
- **Gemma 4:** The bot uses `gemma-4-26b-a4b-it` for AI features.
- **FFmpeg:** Required for music functionality. Windows users need `ffmpeg.exe` in the path or project root.
- **Temp Files:** Use `core.config.TMP_BASE` for temporary file storage.
