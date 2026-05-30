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

"""Unit tests for the admin check module."""

from unittest.mock import AsyncMock, MagicMock, patch

import discord
import pytest

from src.core.admin_check import admin_check, admin_check_slash

TEST_ADMIN_ID = 123456789


@pytest.fixture
def mock_ctx() -> AsyncMock:
    """Fixture for mocking discord.Context."""
    ctx = AsyncMock()
    ctx.message = AsyncMock()
    ctx.author = MagicMock(spec=discord.Member)
    ctx.author.id = 0
    return ctx


@pytest.fixture
def mock_interaction() -> AsyncMock:
    """Fixture for mocking discord.Interaction."""
    interaction = AsyncMock(spec=discord.Interaction)
    interaction.user = MagicMock(spec=discord.Member)
    interaction.user.id = 0
    interaction.response = AsyncMock()
    return interaction


@pytest.mark.asyncio
async def test_admin_check_success(mock_ctx: AsyncMock) -> None:
    """Test successful admin check."""
    mock_ctx.author.id = TEST_ADMIN_ID

    with (
        patch("src.core.admin_check.ADMINS", [TEST_ADMIN_ID]),
        patch("discord.ext.commands.check") as mock_check,
    ):
        admin_check()
        predicate = mock_check.call_args[0][0]

        result = await predicate(mock_ctx)

        assert result is True
        mock_ctx.send.assert_not_called()


@pytest.mark.asyncio
async def test_admin_check_not_admin_with_send(mock_ctx: AsyncMock) -> None:
    """Test admin check for non-admin with message sending."""
    mock_ctx.author.id = 999

    with (
        patch("src.core.admin_check.ADMINS", [TEST_ADMIN_ID]),
        patch("asyncio.sleep", return_value=None),
        patch("discord.ext.commands.check") as mock_check,
    ):
        admin_check()
        predicate = mock_check.call_args[0][0]

        result = await predicate(mock_ctx)

        assert result is False
        mock_ctx.send.assert_called_once_with(
            "You don't have required permissions to do that.",
        )
        mock_ctx.message.delete.assert_called_once()
        mock_ctx.send.return_value.delete.assert_called_once()


@pytest.mark.asyncio
async def test_admin_check_not_admin_no_send(mock_ctx: AsyncMock) -> None:
    """Test admin check for non-admin without message sending."""
    mock_ctx.author.id = 999

    if hasattr(mock_ctx, "send"):
        del mock_ctx.send

    mock_interaction = AsyncMock()
    mock_ctx.interaction = mock_interaction
    resp_mock = mock_interaction.response

    with (
        patch("src.core.admin_check.ADMINS", [TEST_ADMIN_ID]),
        patch("discord.ext.commands.check") as mock_check,
    ):
        admin_check()
        predicate = mock_check.call_args[0][0]

        result = await predicate(mock_ctx)

        assert result is False
        resp_mock.send_message.assert_called_once_with(
            "You don't have required permissions to do that.",
            ephemeral=True,
        )


@pytest.mark.asyncio
async def test_admin_check_slash_admin_success(mock_interaction: AsyncMock) -> None:
    """Test successful slash admin check for admin."""
    mock_interaction.user.id = TEST_ADMIN_ID

    with (
        patch("src.core.admin_check.ADMINS", [TEST_ADMIN_ID]),
        patch("discord.app_commands.check") as mock_check,
    ):
        admin_check_slash()
        predicate = mock_check.call_args[0][0]

        result = await predicate(mock_interaction)

        assert result is True
        mock_interaction.response.send_message.assert_not_called()


@pytest.mark.asyncio
async def test_admin_check_slash_not_admin(mock_interaction: AsyncMock) -> None:
    """Test slash admin check for non-admin."""
    mock_interaction.user.id = 999

    with (
        patch("src.core.admin_check.ADMINS", [TEST_ADMIN_ID]),
        patch("discord.app_commands.check") as mock_check,
    ):
        admin_check_slash()
        predicate = mock_check.call_args[0][0]
        result = await predicate(mock_interaction)

        assert result is False
        mock_interaction.response.send_message.assert_called_once_with(
            "You don't have required permissions to do that.",
            ephemeral=True,
        )
