# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Unit tests for the cowsay module."""

from core.config import COWSAY_SLICE_LIMIT
from src.core.cowsay import cowsay


def test_cowsay_pass() -> None:
    """Test basic cowsay functionality."""
    cowsay_pass = cowsay("Hello World")
    assert "Hello World" in cowsay_pass


def test_cowsay_empty() -> None:
    """Test cowsay with empty input."""
    cowsay_empty = cowsay("")
    assert "What should I say?" in cowsay_empty


def test_cowsay_codeblock() -> None:
    """Test cowsay with codeblocks in input."""
    cowsay_codeblock = cowsay("Say ``` test")
    assert cowsay_codeblock.count("```") == 2


def test_cowsay_slicing() -> None:
    """Test cowsay slicing after string is too long."""
    cowsay_long_input = "a" * 2000
    cowsay_run = cowsay(cowsay_long_input)
    assert cowsay_long_input[:COWSAY_SLICE_LIMIT] + "..." in cowsay_run
