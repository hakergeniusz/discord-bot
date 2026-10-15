# PR Workflow Demo (terminal-browser)

This is a demo pull request to showcase the GitHub PR workflow.

Created: 2026-10-15
Flow demonstrated:
1. Branch from `main` (`demo/pr-workflow-*`)
2. Small docs-only change (this file — no code, no lint risk)
3. `uv run ruff check .`, `uv run ruff format --check .`, `uv run pytest` green
4. Push branch, open PR via GitHub web UI (terminal-browser as `@hakergeniusz-alt`)
5. CI runs, review, merge.

No functional changes — safe to merge or close.

Made by AI (pi agent demo).
