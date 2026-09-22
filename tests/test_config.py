# Copyright (c) 2025-present hakergeniusz
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

"""Unit tests for the config file.

Yes, it is possible - hakergeniusz.
"""

import importlib
from unittest.mock import patch

import src.core.config as config_module


def test_missing_config_file_uses_defaults() -> None:
    """Test default ADMINS and PREFIX when config.yaml is missing."""
    try:
        with patch("pathlib.Path.exists", return_value=False):
            importlib.reload(config_module)
            assert config_module.ADMINS == []
            assert config_module.PREFIX == "!"
    finally:
        importlib.reload(config_module)
