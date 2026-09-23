# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Module for miscellaneous commands such as ping and license information."""

import typing

import discord
from discord.ext import commands


class Other(commands.Cog):
    """Cog for miscellaneous commands like ping and legal info."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the Other cog."""
        self.bot = bot

    @commands.hybrid_command(
        name="ping",
        description="Pong! Outputs the latency of the bot.",
    )
    @typing.override
    async def ping(self, ctx: commands.Context) -> None:
        """Outputs the latency of the bot."""
        latency = round(self.bot.latency * 1000)
        await ctx.reply(f"Pong! Latency is {latency}ms")

    @commands.hybrid_command(name="source", description="Source of the bot.")
    @typing.override
    async def source(self, ctx: commands.Context) -> None:
        """Sends the source code link of the bot."""
        if not ctx.interaction:
            await ctx.send(
                "This bot is open-source! You can find the source here: "
                "https://github.com/hakergeniusz/discord-bot",
            )
            return
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="View Source Code",
                url="https://github.com/hakergeniusz/discord-bot",
            ),
        )
        await ctx.send(
            "This bot is open-source! You can find the source by clicking the following button:",
            view=view,
        )

    @commands.hybrid_command(name="license", description="Bot's license information.")
    @typing.override
    async def licence(self, ctx: commands.Context) -> None:
        """Sends the bot's license information."""
        if not ctx.interaction:
            message = (
                "📜 **Legal Information & License**\n\n"
                "**Copyright (c) 2025-present hakergeniusz**\n"
                "This program is free software: you can redistribute it and/or "
                "modify it under the terms of the **EUPL-1.2** "
                "as published by the European Commission.\n\n"
                "⚠️ Disclaimer of Warranty\n"
                "This program is distributed in the hope that it will be useful, "
                "but **WITHOUT ANY WARRANTY**; without even the implied warranty "
                "of **MERCHANTABILITY** or **FITNESS FOR A PARTICULAR PURPOSE**. "
                "See the [EUPL-1.2](https://joinup.ec.europa.eu/software/page/eupl) "
                "for more details."
            )
            await ctx.send(message)
            return
        embed = discord.Embed(
            title="📜 Legal Information & License",
            color=discord.Color.blue(),
            description=(
                "**Copyright (c) 2025-present hakergeniusz**\n\n"
                "This program is free software: you can redistribute it and/or "
                "modify it under the terms of the **EUPL-1.2** "
                "as published by the European Commission.\n\n"
                "### ⚠️ Disclaimer of Warranty\n"
                "This program is distributed in the hope that it will be useful, "
                "but **WITHOUT ANY WARRANTY**; without even the implied warranty "
                "of **MERCHANTABILITY** or **FITNESS FOR A PARTICULAR PURPOSE**. "
                "See the [EUPL-1.2](https://joinup.ec.europa.eu/software/page/eupl) "
                "for more details."
            ),
        )
        view = discord.ui.View()
        view.add_item(
            discord.ui.Button(
                label="View Source Code",
                url="https://github.com/hakergeniusz/discord-bot",
            ),
        )
        await ctx.send(embed=embed, view=view)


async def setup(bot: commands.Bot) -> None:
    """Add Other cog to the bot."""
    await bot.add_cog(Other(bot))
