# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Discord bot cogs package.

This package contains the various Cog modules that implement command
groups for the bot.  Each module defines a :class:`discord.ext.commands.Cog`
subclass and is dynamically loaded by :mod:`src.main` during bot
initialisation.  The cogs provide administrative commands, music
functionality, fun utilities, error handling, and other modular
features.

The package is intentionally kept lightweight - it only imports the
submodules when required, allowing the bot to start up quickly and to
reload cogs without restarting the whole process.
"""
