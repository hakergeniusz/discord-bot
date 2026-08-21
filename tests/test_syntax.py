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
