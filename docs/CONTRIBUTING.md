# Contributing to discord-bot

Thank you for considering contributing!

## Contributor License Agreement (CLA)
By submitting a Pull Request to this repository, you agree that:
1. You have the right to submit this code.
2. You grant the project maintainer (**hakergeniusz**) the right to redistribute your
   contribution under the current license (EUPL-1.2)
3. You grant the project maintainer the right to change the project's license to any other
   **Open Source license** (as defined by the OSI), **Free Software license** (as defined by the
   Free Software Foundation), or source-available license in the future, without requiring
   additional consent.
4. Your name/username will be preserved as the author of your specific contribution.

## How to contribute
- Fork the repo.
- Create a new branch for your feature or bugfix.
- Submit a Pull Request.

## AI policy

You may use LLMs, vibe-coding, and autonomous agents (including Claude, Codex,
OpenCode, and local models). AI-assisted contributions and PRs written entirely by AI are
welcome, as are branches and PRs opened by autonomous agents.

Requirements:
1. All tests must pass: `uv run pytest` must finish without errors.
2. Read and follow `AGENTS.md` before contributing.
3. Work carried out by an autonomous AI agent, or written entirely by AI, must include an
   `Assisted-by` trailer naming the harness or agent tool and the model, in this format:
   `Assisted-by: [Harness/agent tool name] ([model name])` (for example,
   `Assisted-by: Codex (gpt-6-luna)`).
4. Changes of 200 or more lines in `src/cogs/` must be tested on a Discord client, and the
   relevant `discord.py` documentation must be reviewed.