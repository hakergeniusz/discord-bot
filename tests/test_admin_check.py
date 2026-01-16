import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import discord
from discord.ext import commands
from src.core.admin_check import admin_check, admin_check_slash

TEST_OWNER_ID = 123456789

@pytest.fixture
def mock_ctx():
    ctx = AsyncMock()
    ctx.message = AsyncMock()
    ctx.author = MagicMock(spec=discord.Member)
    ctx.author.id = 0
    return ctx


@pytest.fixture
def mock_interaction():
    interaction = AsyncMock(spec=discord.Interaction)
    interaction.user = MagicMock(spec=discord.Member)
    interaction.user.id = 0
    interaction.response = AsyncMock()
    return interaction


@pytest.mark.asyncio
async def test_admin_check_owner_success(mock_ctx):
    mock_ctx.author.id = TEST_OWNER_ID

    with patch("src.core.admin_check.OWNER_ID", TEST_OWNER_ID):
        with patch("discord.ext.commands.check") as mock_check:
            admin_check()
            predicate = mock_check.call_args[0][0]

            result = await predicate(mock_ctx)

            assert result is True
            mock_ctx.send.assert_not_called()


@pytest.mark.asyncio
async def test_admin_check_not_owner_with_send(mock_ctx):
    mock_ctx.author.id = 999

    with patch("src.core.admin_check.OWNER_ID", TEST_OWNER_ID):
        with patch("asyncio.sleep", return_value=None):
            with patch("discord.ext.commands.check") as mock_check:
                admin_check()
                predicate = mock_check.call_args[0][0]

                result = await predicate(mock_ctx)

                assert result is False
                mock_ctx.send.assert_called_once_with("You don't have required permissions to do that.")
                mock_ctx.message.delete.assert_called_once()
                mock_ctx.send.return_value.delete.assert_called_once()


@pytest.mark.asyncio
async def test_admin_check_not_owner_no_send(mock_ctx):
    mock_ctx.author.id = 999
    del mock_ctx.send
    mock_ctx.response = AsyncMock()

    with patch("src.core.admin_check.OWNER_ID", TEST_OWNER_ID):
        with patch("discord.ext.commands.check") as mock_check:
            admin_check()
            predicate = mock_check.call_args[0][0]

            result = await predicate(mock_ctx)

            assert result is False
            mock_ctx.response.send_message.assert_called_once_with("You don't have required permissions to do that.", ephemeral=True)


@pytest.mark.asyncio
async def test_admin_check_slash_owner_success(mock_interaction):
    mock_interaction.user.id = TEST_OWNER_ID

    with patch("src.core.admin_check.OWNER_ID", TEST_OWNER_ID):
        with patch("discord.app_commands.check") as mock_check:
            admin_check_slash()
            predicate = mock_check.call_args[0][0]

            result = await predicate(mock_interaction)

            assert result is True
            mock_interaction.response.send_message.assert_not_called()


@pytest.mark.asyncio
async def test_admin_check_slash_not_owner(mock_interaction):
    mock_interaction.user.id = 999

    with patch("src.core.admin_check.OWNER_ID", TEST_OWNER_ID):
        with patch("discord.app_commands.check") as mock_check:
            admin_check_slash()
            predicate = mock_check.call_args[0][0]

            result = await predicate(mock_interaction)

            assert result is False
            mock_interaction.response.send_message.assert_called_once_with("You don't have required permissions to do that.", ephemeral=True)
