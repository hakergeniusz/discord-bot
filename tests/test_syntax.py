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

import os
import py_compile
import pytest

def get_python_files():
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
    python_files = []
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

@pytest.mark.parametrize("filepath", get_python_files())
def test_python_syntax(filepath):
    """Attempt to compile each file to check for syntax errors."""
    try:
        py_compile.compile(filepath, doraise=True)
    except py_compile.PyCompileError as e:
        pytest.fail(f"Syntax error in {filepath}: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error when compiling {filepath}: {e}")
