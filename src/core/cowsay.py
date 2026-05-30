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

"""Module for generating ASCII art of a cow saying text."""

from core.config import COWSAY_SLICE_LIMIT, FULL_COWSAY_LIMIT


def cowsay(text: str) -> str:
    """A simple cowsay.

    Args:
        text (str): Text for the cow to say. Any ``` will be removed.

    Returns:
        str: Cow in a code block that says the *text* argument.
    """
    if not text or text.isspace():
        return (
            "```\n"
            " __________________ \n"
            "< What should I say? >\n"
            " ------------------ \n"
            r"        \   ^__^"
            "\n"
            r"         \  (oo)\_______"
            "\n"
            r"            (__)\       )\\/\\"
            "\n"
            r"                ||----w |"
            "\n"
            r"                ||     ||"
            "\n"
            "```"
        )
    text = text.replace("```", "` ` `")

    if len(text) > FULL_COWSAY_LIMIT:
        text = text[:COWSAY_SLICE_LIMIT] + "..."

    lines = text.splitlines()
    if not lines:
        text = "..."
        lines = [text]

    width = max(len(line) for line in lines)

    top_bottom = " " + "_" * (width + 2)
    bubble_content = [f"< {line.ljust(width)} >" for line in lines]

    bubble = "\n".join(bubble_content)
    divider = " " + "-" * (width + 2)

    cow_art = rf"""{top_bottom}
{bubble}
{divider}
        \   ^__^
         \  (oo)\_______
            (__)\       )\\/\\
                ||----w |
                ||     ||"""
    return f"```\n{cow_art}\n```"
