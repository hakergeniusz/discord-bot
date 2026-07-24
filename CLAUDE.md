# CLAUDE.md

Guidance for AI agents working on this repository.

## Project

A feature-rich Discord bot built with `discord.py`. Commands are exposed as **hybrid commands** (both prefix `!` and slash). AI features use Google GenAI (Gemma models).

- **Language:** Python 3.14+ (strict typing, modern features)
- **Framework:** `discord.py` >= 2.6.4
- **AI:** `google-genai` (Gemma 4 models)
- **Music:** `yt-dlp` + FFmpeg
- **Tooling:** `uv` (deps), `ruff` (lint/format), `pytest` (tests, `pytest-asyncio`)
- **License:** EUPL-1.2 — a copyright header is **mandatory on every file** (see Conventions)

## Commands

All tooling runs through `uv` (deps are dev-group, not on PATH):

```bash
uv sync                       # install / update deps from uv.lock
uv run ruff format src tests  # format
uv run ruff check src tests   # lint (ALL ruleset, line-length 100)
uv run pytest                 # run tests
uv run bot                    # run the bot (reads .env + config.yaml)
```

Format + lint are also applied automatically after edits via the `PostToolUse` hook in `.claude/settings.json`.

## Architecture

```
src/main.py        Entry point. MyBot(commands.Bot) + automatic cog loader that walks src/cogs/.
src/cogs/          Discord layer: commands & event listeners (admin, music, fun, utility, other,
                   on_startup, error_handler). Thin — delegate work to core/.
src/core/          Pure-Python logic, decoupled from Discord objects (Context/Message) where possible:
                   ai, config, logger, admin_check, f1, youtube, image_checker, cowsay, howmany.
tests/             Mirror of src modules (test_*.py), asyncio_mode = auto.
config.yaml        Bot config (prefix, admin user IDs). Secrets -> .env.
```

**Rules**
- Prefer `commands.hybrid_command` so commands work as both prefix and slash.
- Use `app_commands.describe` for parameter docs.
- Use `ctx.defer()` for commands taking >3s.
- Heavy processing / external API calls belong in `src/core/`, not in cogs.
- Permission checks via `@admin_check()` (see `src/core/admin_check.py`).

## Conventions

- **Copyright header (MANDATORY at the top of every file):** enforced automatically by ruff's `CPY001` rule — a missing/incorrect header fails `uv run ruff check`.
  ```python
  # Copyright (c) 2025-2026 hakergeniusz
  #
  # Licensed under the EUPL, Version 1.2 or - as soon they will be approved by the European
  # Commission - subsequent versions of the EUPL (the "Licence"); You may not use this work
  # except in compliance with the Licence.
  #
  # You may obtain a copy of the Licence at:
  # https://joinup.ec.europa.eu/software/page/eupl
  #
  # Unless required by applicable law or agreed to in writing, software distributed under
  # the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF
  # ANY KIND, either express or implied. See the Licence for the specific language
  ```
- **Lint/format:** `ruff` with the `ALL` ruleset (minor ignores in `pyproject.toml`), line-length 100.
- **Docstrings:** Google style, required for classes and public methods.
- **Types:** strict type hints on all signatures and complex variables; use `TYPE_CHECKING` for circular imports.
- **Errors:** no silent failures — log via `src/core/logger.py` or surface to the user via `src/cogs/error_handler.py`.
- **Temp files:** use `core.config.TMP_BASE`.

## Notes / gotchas

- Requires Python 3.14+.
- FFmpeg must be installed for music commands.
- `.env` holds secrets (e.g. `GOOGLE_API_KEY`); `config.yaml` holds non-secret bot config. Both are gitignored / excluded.
- CI runs `pytest` on every push (`.github/workflows/tests.yml`).

## Commits

**Commits must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.**  
Format: `<type>[optional scope]: <description>` — e.g. `feat: add music queue command`.

Every commit message must end with a `Co-authored-by` trailer for Claude, separated from the
body by a single blank line, exactly as GitHub expects:

```text
<type>[optional scope]: <description>

<optional body>

Co-authored-by: Claude <noreply@anthropic.com>
```

- The trailer is on its own line, preceded by exactly one blank line.
- When Claude makes a commit, it appends this trailer automatically.
