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

"""Tests for the on_startup cog."""

from unittest.mock import AsyncMock, MagicMock

import discord
import pytest
from discord.ext import commands

from cogs.on_startup import SyncCog


@pytest.mark.asyncio
async def test_on_ready_sync() -> None:
    """Test on_ready synchronization."""
    bot = MagicMock(spec=commands.Bot)
    bot.tree = AsyncMock()
    bot.change_presence = AsyncMock()
    cog = SyncCog(bot)

    await cog.on_ready()

    bot.tree.sync.assert_called_once()
    bot.change_presence.assert_called_once()
    _args, kwargs = bot.change_presence.call_args
    assert kwargs["status"] == discord.Status.dnd
