# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

"""Unit tests for syntax validation of source files."""

import py_compile
from pathlib import Path

import pytest


def get_python_files() -> list[str]:
    """Get all Python files in the src directory.

    Returns:
        list[str]: List of file paths as strings.
    """
    src_dir = Path(__file__).resolve().parent.parent / "src"
    return [str(path) for path in src_dir.rglob("*.py")]


@pytest.mark.parametrize("filepath", get_python_files())
def test_python_syntax(filepath: str) -> None:
    """Attempt to compile each file to check for syntax errors."""
    py_compile.compile(filepath, doraise=True)
