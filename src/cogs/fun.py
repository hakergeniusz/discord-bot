# Copyright (C) 2026 hakergeniusz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio

import discord
from discord import app_commands
from discord.ext import commands

from core.config import CURRENT_YEAR, RICKROLL_GIF_URL, TMP_BASE
from core.cowsay import cowsay
from core.f1 import f1_season_calendar, f1_standings_py, race_result
from core.howmany import change_file


class F1Commands(commands.Cog):
    """Cog for Formula 1 related commands."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the F1Commands cog."""
        self.bot = bot

    @commands.hybrid_command(
        name="f1_race_result", description="Outputs the result of an F1 race"
    )
    @app_commands.describe(
        season="Season of the race you want the result of",
        roundnumber="Round number of the race asked. You can get one with /f1_calendar",
        emojis="Default is True, if False, emojis for podium positions "
        "will not be given.",
    )
    # Remember to change *roundnumber* if F1 introduces an F1 calendar
    # with more than 24 rounds.
    async def f1_race_result(
        self,
        ctx: commands.Context,
        season: commands.Range[int, 1950, CURRENT_YEAR],
        roundnumber: commands.Range[int, 1, 24],
        emojis: bool = True,
    ) -> None:
        """Gives the result of an F1 race asked for."""
        await ctx.defer()
        grand_prix_name, results_list = await race_result(
            season=season, roundnumber=roundnumber, emojis=emojis
        )
        if grand_prix_name is None or results_list == []:
            await ctx.send(f"Could not find R{roundnumber} in {season} F1 season.")
            return
        results = "\n".join(results_list)
        response_f1 = discord.Embed(
            title=f"F1 {grand_prix_name} ({season})",
            description=results,
            color=discord.Color.red(),
        )
        await ctx.send(embed=response_f1)

    @commands.hybrid_command(name="f1_calendar", description="Shows an F1 calendar")
    @app_commands.describe(season="Season of the calendar you want to know")
    async def f1_calendar(
        self, ctx: commands.Context, season: commands.Range[int, 1950, CURRENT_YEAR]
    ) -> None:
        """Shows the F1 calendar for a specific season."""
        await ctx.defer()
        calendar_list = await f1_season_calendar(season)
        if calendar_list == []:
            await ctx.send(f"No calendar found for {season}.")
            return
        calendar = "\n".join(calendar_list)
        if not ctx.interaction:
            message = f"""
**F1 {season} calendar:**
{calendar}
            """
            await ctx.send(message)
            return

        f1_calendar = discord.Embed(
            title=f"F1 {season} calendar",
            description=calendar,
            color=discord.Color.red(),
        )
        await ctx.send(embed=f1_calendar)

    @commands.hybrid_command(
        name="f1_standings", description="Shows F1 standings for a season."
    )
    @app_commands.describe(season="Season you want standings for.")
    async def f1_standings(
        self, ctx: commands.Context, season: commands.Range[int, 1950, CURRENT_YEAR]
    ) -> None:
        """Shows F1 standings for a specific season."""
        await ctx.defer()
        standings_list = await f1_standings_py(season)
        if standings_list == []:
            await ctx.send(f"No standings found for {season}.")
            return
        standings = "\n".join(standings_list)
        if not ctx.interaction:
            message = f"**F1 {season} standings:**\n{standings}"
            await ctx.send(message)
            return

        f1_standings = discord.Embed(
            title=f"F1 {season} standings",
            description=standings,
            color=discord.Color.red(),
        )
        await ctx.send(embed=f1_standings)


class HowManyButtonButtons(discord.ui.View):
    """A class for ```/howmanybutton``` to work."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the HowManyButtonButtons view."""
        super().__init__()
        self.bot = bot

    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.success)
    async def howmanybutton_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        """Increment count when the button is clicked."""
        from pathlib import Path

        count = await asyncio.to_thread(
            change_file, str(Path(TMP_BASE) / "howmanybutton"), interaction.user.id
        )
        suffix = "time" if count == 1 else "times"
        msg = f"{interaction.user.mention} clicked the button {count} {suffix}!"
        await interaction.response.edit_message(content=msg)


class Meme(commands.Cog):
    """Cog for meme and fun commands."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the Meme cog."""
        self.bot = bot

    @commands.hybrid_command(name="nothing", description=".")
    async def nothing(self, ctx: commands.Context) -> None:
        """Literally nothing."""
        await ctx.send(".", ephemeral=True)
        print(f"{ctx.author.name} tried nothing...")

    @commands.hybrid_command(
        name="howmanytimes", description="Says how many times was the command typed"
    )
    async def howmanytimes(self, ctx: commands.Context) -> None:
        """Says how many times this user typed this command."""
        from pathlib import Path

        count = await asyncio.to_thread(
            change_file, str(Path(TMP_BASE) / "howmanytimes"), ctx.author.id
        )
        suffix = "time" if count == 1 else "times"
        await ctx.send(f"You have used this command {count} {suffix}!")

    @commands.hybrid_command(name="complain", description="Compain to the bot owner.")
    async def complain(self, ctx: commands.Context) -> None:
        """Sends a rickroll GIF when someone tries to complain."""
        await ctx.send(RICKROLL_GIF_URL, ephemeral=True)
        print(f"{ctx.author.name} complained and regretted it.")

    @commands.hybrid_command(name="heart", description="Shows a heart.")
    async def heart(self, ctx: commands.Context) -> None:
        """Shows a middle finger emoji."""
        await ctx.send(":middle_finger:", ephemeral=True)

    @commands.hybrid_command(name="finger", description="Shows a finger.")
    async def finger(self, ctx: commands.Context) -> None:
        """Shows a heart emoji."""
        await ctx.send(":heart:", ephemeral=True)

    @commands.hybrid_command(name="rickroll_me", description="Rickrolls the user.")
    async def rickroll(self, ctx: commands.Context) -> None:
        """Rickrolls the user."""
        await ctx.send("Ok, if you want to be rickrolled, you will be.")
        await ctx.send(RICKROLL_GIF_URL)

    @app_commands.command(
        name="howmanybutton", description="How many times did you press the button?"
    )
    async def howmanybutton(self, interaction: discord.Interaction) -> None:
        """Sends a message with a button that tracks global clicks.

        Globally tracks how many times users clicked the button.
        """
        view = HowManyButtonButtons(interaction.client)
        await interaction.response.send_message("Click this button!", view=view)

    @commands.hybrid_command(name="cowsay", description="I'm a cow!")
    @app_commands.describe(text="What you want me to say?")
    async def cowsay(self, ctx: commands.Context, *, text: str = None) -> None:
        """I'm a cow! Sends text wrapped in cowsay."""
        if text and len(text) >= 250:
            await ctx.send("You can't say that much!")
            return
        await ctx.send(cowsay(text))

    @commands.command(name="nvidia")
    async def nvidia(self, ctx: commands.Context) -> None:
        """Sends the Linus Torvalds NVIDIA GIF."""
        await ctx.reply(
            "https://tenor.com/view/linus-linus-torvalds-nvidia-fuck-you-gif-18053606",
            mention_author=False,
        )


async def setup(bot: commands.Bot) -> None:
    """Add F1Commands and Meme cogs to the bot."""
    await bot.add_cog(F1Commands(bot))
    await bot.add_cog(Meme(bot))
