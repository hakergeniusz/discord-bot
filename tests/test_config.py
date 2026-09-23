# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

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
