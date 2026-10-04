# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Tests for Fun and F1 cogs."""

from unittest.mock import AsyncMock, MagicMock, patch

import discord
import pytest
from discord.ext import commands

from cogs.fun import F1Commands, HowManyButtonButtons, Meme, setup
from core.config import RICKROLL_GIF_URL


def _make_ctx() -> AsyncMock:
    """Build a Context double for hybrid commands.

    Returns:
        AsyncMock: Context double ready for command callbacks.
    """
    ctx = AsyncMock(spec=commands.Context)
    ctx.interaction = None
    ctx.author = MagicMock()
    ctx.author.id = 456
    return ctx


def test_f1_commands_init() -> None:
    """Test F1Commands initialization."""
    bot = MagicMock(spec=discord.ext.commands.Bot)
    cog = F1Commands(bot)
    assert cog.bot == bot


def test_meme_init() -> None:
    """Test Meme cog initialization."""
    bot = MagicMock(spec=discord.ext.commands.Bot)
    cog = Meme(bot)
    assert cog.bot == bot


@pytest.mark.asyncio
async def test_howmanybutton_button_callback() -> None:
    """Test howmanybutton button callback."""
    bot = MagicMock(spec=discord.ext.commands.Bot)
    view = HowManyButtonButtons(bot)
    interaction = AsyncMock(spec=discord.Interaction)
    interaction.user.id = 123
    interaction.user.mention = "<@123>"
    interaction.response = AsyncMock()

    # Mocking change_file since it's an external dependency
    with patch("cogs.fun.change_file", return_value=1):
        await view.howmanybutton_button.callback(interaction)

    interaction.response.edit_message.assert_called_once()
    edit_message = interaction.response.edit_message
    assert "<@123> clicked the button 1 time!" in edit_message.call_args.kwargs["content"]


@pytest.mark.asyncio
async def test_meme_heart() -> None:
    """Test Meme.heart command."""
    cog = Meme(MagicMock())
    ctx = AsyncMock(spec=commands.Context)

    await cog.heart.callback(cog, ctx)
    ctx.send.assert_called_with(":middle_finger:", ephemeral=True)


@pytest.mark.asyncio
async def test_meme_finger() -> None:
    """Test Meme.finger command."""
    cog = Meme(MagicMock())
    ctx = AsyncMock(spec=commands.Context)

    await cog.finger.callback(cog, ctx)
    ctx.send.assert_called_with(":heart:", ephemeral=True)


@pytest.mark.asyncio
async def test_meme_archbtw() -> None:
    """Test Meme.archbtw command."""
    cog = Meme(MagicMock())
    ctx = AsyncMock(spec=commands.Context)

    await cog.archbtw.callback(cog, ctx)
    ctx.reply.assert_called_with("I use Arch btw")


@pytest.mark.asyncio
async def test_f1_race_result_not_found() -> None:
    """Test f1_race_result when the round does not exist."""
    cog = F1Commands(MagicMock())
    ctx = _make_ctx()

    with patch("cogs.fun.race_result", new=AsyncMock(return_value=(None, []))):
        await cog.f1_race_result.callback(cog, ctx, 2024, 5)

    ctx.send.assert_called_with("Could not find R5 in 2024 F1 season.")


@pytest.mark.asyncio
async def test_f1_race_result_sends_embed() -> None:
    """Test f1_race_result rendering the podium."""
    cog = F1Commands(MagicMock())
    ctx = _make_ctx()
    results = ["1. Max Verstappen", "2. Lando Norris"]

    with patch("cogs.fun.race_result", new=AsyncMock(return_value=("Monaco GP", results))):
        await cog.f1_race_result.callback(cog, ctx, 2024, 8, emojis=False)

    embed = ctx.send.call_args.kwargs["embed"]
    assert embed.title == "F1 Monaco GP (2024)"
    assert results[0] in embed.description


@pytest.mark.asyncio
async def test_f1_qualifying_not_found() -> None:
    """Test f1_qualifying_result when the round does not exist."""
    cog = F1Commands(MagicMock())
    ctx = _make_ctx()

    with patch("cogs.fun.f1_qualifying", new=AsyncMock(return_value=(None, []))):
        await cog.f1_qualifying_result.callback(cog, ctx, 2024, 6)

    ctx.send.assert_called_with("Could not find R6 in 2024 F1 season.")


@pytest.mark.asyncio
async def test_f1_qualifying_sends_embed() -> None:
    """Test f1_qualifying_result rendering the qualifying order."""
    cog = F1Commands(MagicMock())
    ctx = _make_ctx()

    with patch(
        "cogs.fun.f1_qualifying",
        new=AsyncMock(return_value=("British GP", ["P1. Max", "P2. Lando"])),
    ):
        await cog.f1_qualifying_result.callback(cog, ctx, 2024, 6)

    embed = ctx.send.call_args.kwargs["embed"]
    assert embed.title == "F1 Qualifying British GP (2024)"


@pytest.mark.asyncio
async def test_f1_calendar_empty() -> None:
    """Test f1_calendar when no calendar is available."""
    cog = F1Commands(MagicMock())
    ctx = _make_ctx()

    with patch("cogs.fun.f1_season_calendar", new=AsyncMock(return_value=[])):
        await cog.f1_calendar.callback(cog, ctx, 2030)

    ctx.send.assert_called_with("No calendar found for 2030.")


@pytest.mark.asyncio
async def test_f1_calendar_without_interaction() -> None:
    """Test f1_calendar sending plain text outside an interaction."""
    cog = F1Commands(MagicMock())
    ctx = _make_ctx()

    with patch("cogs.fun.f1_season_calendar", new=AsyncMock(return_value=["R1 Bahrain"])):
        await cog.f1_calendar.callback(cog, ctx, 2024)

    message = ctx.send.call_args.args[0]
    assert "R1 Bahrain" in message
    assert "embed" not in ctx.send.call_args.kwargs


@pytest.mark.asyncio
async def test_f1_calendar_with_interaction() -> None:
    """Test f1_calendar sending an embed inside an interaction."""
    cog = F1Commands(MagicMock())
    ctx = _make_ctx()
    ctx.interaction = AsyncMock()

    with patch("cogs.fun.f1_season_calendar", new=AsyncMock(return_value=["R1 Bahrain"])):
        await cog.f1_calendar.callback(cog, ctx, 2024)

    embed = ctx.send.call_args.kwargs["embed"]
    assert embed.title == "F1 2024 calendar"
    assert "R1 Bahrain" in embed.description


@pytest.mark.asyncio
async def test_f1_standings_empty() -> None:
    """Test f1_standings when no standings are available."""
    cog = F1Commands(MagicMock())
    ctx = _make_ctx()

    with patch("cogs.fun.f1_standings_py", new=AsyncMock(return_value=[])):
        await cog.f1_standings.callback(cog, ctx, 2024)

    ctx.send.assert_called_with("No standings found for 2024.")


@pytest.mark.asyncio
async def test_f1_standings_without_interaction() -> None:
    """Test f1_standings sending plain text outside an interaction."""
    cog = F1Commands(MagicMock())
    ctx = _make_ctx()

    with patch("cogs.fun.f1_standings_py", new=AsyncMock(return_value=["1. Max - 100 pts"])):
        await cog.f1_standings.callback(cog, ctx, 2024)

    message = ctx.send.call_args.args[0]
    assert "**F1 2024 standings:**" in message
    assert "1. Max - 100 pts" in message


@pytest.mark.asyncio
async def test_f1_standings_with_interaction() -> None:
    """Test f1_standings sending an embed inside an interaction."""
    cog = F1Commands(MagicMock())
    ctx = _make_ctx()
    ctx.interaction = AsyncMock()

    with patch("cogs.fun.f1_standings_py", new=AsyncMock(return_value=["1. Max - 100 pts"])):
        await cog.f1_standings.callback(cog, ctx, 2024)

    assert ctx.send.call_args.kwargs["embed"].title == "F1 2024 standings"


@pytest.mark.asyncio
async def test_meme_nothing() -> None:
    """Test Meme.nothing sending a dot."""
    cog = Meme(MagicMock())
    ctx = _make_ctx()

    await cog.nothing.callback(cog, ctx)

    ctx.send.assert_called_with(".", ephemeral=True)


@pytest.mark.asyncio
async def test_meme_complain_rickrolls() -> None:
    """Test Meme.complain sending the rickroll GIF."""
    cog = Meme(MagicMock())
    ctx = _make_ctx()

    await cog.complain.callback(cog, ctx)

    ctx.send.assert_called_with(RICKROLL_GIF_URL, ephemeral=True)


@pytest.mark.asyncio
async def test_meme_rickroll() -> None:
    """Test Meme.rickroll sending the confirmation and the GIF."""
    cog = Meme(MagicMock())
    ctx = _make_ctx()

    await cog.rickroll.callback(cog, ctx)

    assert ctx.send.await_count == 2
    assert ctx.send.await_args_list[-1].args[0] == RICKROLL_GIF_URL


@pytest.mark.asyncio
async def test_meme_nvidia() -> None:
    """Test Meme.nvidia replying with the NVIDIA GIF."""
    cog = Meme(MagicMock())
    ctx = _make_ctx()

    await cog.nvidia.callback(cog, ctx)

    assert "tenor.com" in ctx.reply.call_args.args[0]
    assert ctx.reply.call_args.kwargs["mention_author"] is False


@pytest.mark.asyncio
async def test_meme_cowsay_rejects_long_input() -> None:
    """Test Meme.cowsay rejecting oversized input."""
    cog = Meme(MagicMock())
    ctx = _make_ctx()

    await cog.cowsay.callback(cog, ctx, text="x" * 300)

    ctx.send.assert_called_with("You can't say that much!")


@pytest.mark.asyncio
async def test_meme_cowsay_wraps_input() -> None:
    """Test Meme.cowsay wrapping short input."""
    cog = Meme(MagicMock())
    ctx = _make_ctx()

    with patch("cogs.fun.cowsay", return_value=" MOCKED "):
        await cog.cowsay.callback(cog, ctx, text="moo")

    ctx.send.assert_called_with(" MOCKED ")


@pytest.mark.asyncio
async def test_howmanytimes_singular() -> None:
    """Test howmanytimes using the singular form for the first use."""
    cog = Meme(MagicMock())
    ctx = _make_ctx()

    with patch("cogs.fun.change_file", new=AsyncMock(return_value=1)):
        await cog.howmanytimes.callback(cog, ctx)

    ctx.send.assert_called_with("You have used this command 1 time!")


@pytest.mark.asyncio
async def test_howmanytimes_plural() -> None:
    """Test howmanytimes using the plural form for later uses."""
    cog = Meme(MagicMock())
    ctx = _make_ctx()

    with patch("cogs.fun.change_file", new=AsyncMock(return_value=7)):
        await cog.howmanytimes.callback(cog, ctx)

    ctx.send.assert_called_with("You have used this command 7 times!")


@pytest.mark.asyncio
async def test_howmanybutton_sends_view() -> None:
    """Test howmanybutton attaching the click counter view."""
    cog = Meme(MagicMock())
    interaction = AsyncMock(spec=discord.Interaction)
    interaction.response = AsyncMock()

    await cog.howmanybutton.callback(cog, interaction)

    view = interaction.response.send_message.call_args.kwargs["view"]
    assert isinstance(view, HowManyButtonButtons)


@pytest.mark.asyncio
async def test_howmanybutton_plural_suffix() -> None:
    """Test the button counter using the plural suffix."""
    view = HowManyButtonButtons(MagicMock())
    interaction = AsyncMock(spec=discord.Interaction)
    interaction.user.id = 123
    interaction.user.mention = "<@123>"
    interaction.response = AsyncMock()

    with patch("cogs.fun.change_file", new=AsyncMock(return_value=5)):
        await view.howmanybutton_button.callback(interaction)

    sent = interaction.response.edit_message.call_args.kwargs["content"]
    assert sent == "<@123> clicked the button 5 times!"


@pytest.mark.asyncio
async def test_fun_setup_adds_cogs() -> None:
    """Test that setup registers both the F1 and meme cogs."""
    bot = MagicMock(spec=discord.ext.commands.Bot)
    bot.add_cog = AsyncMock()

    await setup(bot)

    added = [call.args[0] for call in bot.add_cog.await_args_list]
    assert [type(cog) for cog in added] == [F1Commands, Meme]
