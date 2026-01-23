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

import py_compile
from pathlib import Path

import pytest


def get_python_files() -> list[str]:
    """Get all Python files in the src directory."""
    src_dir = Path(__file__).resolve().parent.parent / "src"
    python_files = []
    for path in src_dir.rglob("*.py"):
        python_files.append(str(path))
    return python_files


@pytest.mark.parametrize("filepath", get_python_files())
def test_python_syntax(filepath: str) -> None:
    """Attempt to compile each file to check for syntax errors."""
    try:
        py_compile.compile(filepath, doraise=True)
    except py_compile.PyCompileError as e:
        pytest.fail(f"Syntax error in {filepath}: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error when compiling {filepath}: {e}")
