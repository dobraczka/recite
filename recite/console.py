from dataclasses import dataclass
from typing import Optional

from rich import print as rprint


@dataclass
class ReciteConsole:
    prefix: str = "recite >"
    base_color: str = "white"
    bad_color: str = "red"
    good_color: str = "green"
    bad_glyph: str = "✘ "
    good_glyph: str = "✓ "

    def print(self, message: str, color: str = "white", glyph: str = "", number_str: str = "", indent_count: int = 0, indent_char: str = "*"):
        indent_str = ""
        if indent_count > 0:
            indent_str = " " * indent_count
            indent_str += indent_char + " "
        rprint(
            f"{self.prefix} {number_str}[{color}]{indent_str}{glyph}{message}[/{color}]"
        )

    def print_success(self, message: str, number: Optional[str] = None):
        number_str = ""
        if number:
            number_str = f"{number}: "
        self.print(
            color=self.good_color,
            glyph=self.good_glyph,
            number_str=number_str,
            message=message,
        )

    def print_failure(self, message: str, number: Optional[str] = None):
        number_str = ""
        if number:
            number_str = f"{number}: "
        self.print(
            color=self.bad_color,
            glyph=self.bad_glyph,
            number_str=number_str,
            message=message,
        )

    def print_error(self, message: str, indent_count: str):
        self.print(message=message, indent_count=indent_count, color=self.bad_color)


if __name__ == "__main__":
    console = ReciteConsole()
    console.print_bad("I am a bad message")
    console.print_good("I am a good message")
    console.print("I am a neutral message")
    console.print("I am an indented message", indent_count=1)
    console.print("I am an indented message", indent_count=2)
    console.print("I am an indented message", indent_count=1)
