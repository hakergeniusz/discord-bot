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

"""Unit tests for the cowsay module."""

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
