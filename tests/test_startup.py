# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Smoke tests for bot startup and initialization."""

import pytest

from main import MyBot


@pytest.mark.asyncio
async def test_bot_initialization() -> None:
    """Test that the bot can be initialized and cogs can be loaded."""
    bot = MyBot()
    # Mocking login and other discord-related internals isn't strictly necessary
    # if we just want to test load_cogs which deals with file system and imports.

    # We call load_cogs directly to verify imports and file structure
    await bot.load_cogs()

    # Check if cogs were loaded (extensions is a dict of loaded extensions)
    assert len(bot.extensions) > 0
    assert "cogs.on_startup" in bot.extensions
