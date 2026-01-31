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

"""Module for generating ASCII art of a cow saying text."""


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
            + "\n"
            + r"         \  (oo)\_______"
            + "\n"
            + r"            (__)\       )\\/\\"
            + "\n"
            + r"                ||----w |"
            + "\n"
            + r"                ||     ||"
            + "\n"
            "```"
        )
    text = text.replace("```", "` ` `")

    if len(text) > 1800:
        text = text[:1797] + "..."

    lines = text.splitlines()
    if not lines:
        text = "..."
        lines = [text]

    width = max(len(line) for line in lines)

    top_bottom = " " + "_" * (width + 2)
    bubble_content = []
    for line in lines:
        bubble_content.append(f"< {line.ljust(width)} >")

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
