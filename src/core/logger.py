# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Module for configuring the bot's logging system."""

import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """Creates and returns a configured logger.

    Returns:
        logging.Logger: A configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.propagate = False
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
