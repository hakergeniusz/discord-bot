# Contributing to discord-bot

Thank you for considering contributing!

## Contributor License Agreement (CLA)
By submitting a Pull Request to this repository, you agree that:
1. You have the right to submit this code.
2. You grant the project maintainer (**hakergeniusz**) the right to redistribute your contribution under the current license (EUPL-1.2)
3. You grant the project maintainer the right to change the project's license to any other **Open Source license** (as defined by the OSI) or **Free Software license** (as defined by the Free Software Foundation) or source-available license in the future, without requiring additional consent.
4. Your name/username will be preserved as the author of your specific contribution.

## How to contribute
- Fork the repo.
- Create a new branch for your feature or bugfix.
- Submit a Pull Request.

## AI policy

You may use LLMs, vibe-coding, and autonomous agents (Claude, Codex,
OpenCode, local models, etc.). What matters is the result, not the author.

Allowed:
- AI-assisted or fully AI-written PRs
- Autonomous-agent branches, incl. auto-opened PRs

Requirements (same bar as human code):
1. **It works.** `uv run ruff check .`, `uv run ruff format --check .`
   and `uv run pytest` are green. New logic comes with tests.
2. **No AI slop.** No dead code, placeholder `TODO`s, hallucinated APIs,
   over-abstracted helpers, sycophantic comments, or tests that assert
   nothing (`assert True`, empty mocks, `pass`-only cases).
3. **Follows this repo's shape.** Thin cogs in `src/cogs/`, logic in
   `src/core/`, hybrid commands, EUPL header on new files, `TMP_BASE`
   for temp files, conventional-commit messages.
4. **You are responsible for any bugs.** If the bot breaks in production, "the AI wrote it"
   is not a defense. The submitter is responsible for understanding
   what the PR does.
5. **Disclose fully-AI work.** If a commit was made by an autonomous
   agent or written exclusively by AI, add the trailer from `AGENTS.md`:
   `Co-authored-by: Claude <noreply@anthropic.com>`. Human + AI
   collaboration needs no trailer. For PRs, append "Made by AI" or "Made by [AI model name, agent name etc.]"

Maintainer may close anything that looks unreviewed, untested, or
bulk-generated without discussion - even if CI is green.
