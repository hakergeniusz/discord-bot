# Copyright (c) 2025-present hakergeniusz
# SPDX-License-Identifier: EUPL-1.2

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
