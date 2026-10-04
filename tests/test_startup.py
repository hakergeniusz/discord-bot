# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Smoke tests for bot startup and initialization."""

import sys

import pytest

from main import MyBot


def _restore_modules(before: dict) -> None:
    """Put back modules that were replaced while the test ran.

    discord.py's extension loader re-executes every cog module and rebinds it in
    ``sys.modules``. Test modules import cog classes at collection time, so without this
    a reload leaves ``patch("cogs.<name>...")`` pointing at a module that is no longer
    the one owning the class under test.

    Args:
        before: Mapping of ``sys.modules`` captured before the test ran.
    """
    for name, module in list(sys.modules.items()):
        if name in before and before[name] is not module:
            sys.modules[name] = before[name]


@pytest.mark.asyncio
async def test_bot_initialization() -> None:
    """Test that the bot can be initialized and cogs can be loaded."""
    bot = MyBot()
    # Mocking login and other discord-related internals isn't strictly necessary
    # if we just want to test load_cogs which deals with file system and imports.

    before = dict(sys.modules)
    # We call load_cogs directly to verify imports and file structure
    await bot.load_cogs()
    _restore_modules(before)

    # Check if cogs were loaded (extensions is a dict of loaded extensions)
    assert len(bot.extensions) > 0
    assert "cogs.on_startup" in bot.extensions
