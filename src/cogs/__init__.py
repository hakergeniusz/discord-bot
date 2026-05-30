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

from core.logger import get_logger

logger = get_logger(__name__)
