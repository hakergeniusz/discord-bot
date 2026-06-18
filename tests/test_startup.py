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
# governing permissions and limitations under the Licence.

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
