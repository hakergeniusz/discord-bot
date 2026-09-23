# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Core utilities for the Discord bot.

This package contains the shared logic and configuration helpers used
by the bot's cogs and command handlers.  It provides:

* :mod:`core.config` - environment and YAML configuration loading.
* :mod:`core.admin_check` - decorators that enforce admin-only
  command execution.
* :mod:`core.ai` - integration with Google Gemini.
* :mod:`core.youtube` - helper functions for downloading and
  streaming audio from YouTube.

Only the modules listed above are intended for import.  The package
does not expose any additional public API beyond these submodules.
"""
