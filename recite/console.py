from dataclasses import dataclass
from typing import Iterable, Optional

from rich import print as rprint


@dataclass
class ReciteConsole:
    prefix: str = "recite >"
    base_color: str = "white"
    bad_color: str = "red"
    good_color: str = "green"
    bad_glyph: str = "✘ "
    good_glyph: str = "✓ "

    def print_message(
        self,
        message: str,
        color: str = "white",
        glyph: str = "",
        number_str: str = "",
        indent_count: int = 0,
        indent_char: str = "*",
    ):
        if color.lower() == "bad":
            color = self.bad_color
        elif color.lower() == "good":
            color = self.good_color
        indent_str = ""
        if indent_count > 0:
            indent_str = "\t" * indent_count
            indent_str += indent_char + " "
        rprint(
            f"{self.prefix} {number_str}[{color}]{indent_str}{glyph}{message}[/{color}]"
        )

    def print_multiple_messages(
        self,
        messages: Iterable[str],
        color: str = "white",
        indent_count: int = 0,
        indent_char: str = "*",
    ):
        for msg_n, msg in enumerate(messages):
            if msg_n > 0:
                indent_char = " "
            self.print_message(
                message=msg,
                indent_count=indent_count,
                indent_char=indent_char,
                color=color,
            )

    def print_success(self, message: str, number: Optional[int] = None):
        number_str = ""
        if number:
            number_str = f"{number}: "
        self.print_message(
            color=self.good_color,
            glyph=self.good_glyph,
            number_str=number_str,
            message=message,
        )

    def print_failure(self, message: str, number: Optional[int] = None):
        number_str = ""
        if number:
            number_str = f"{number}: "
        self.print_message(
            color=self.bad_color,
            glyph=self.bad_glyph,
            number_str=number_str,
            message=message,
        )

    def print_error(self, message: str, indent_count: int):
        self.print_message(
            message=message, indent_count=indent_count, color=self.bad_color
        )
