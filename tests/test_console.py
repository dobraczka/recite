# smoketests for console
import pytest

from recite.console import ReciteConsole


@pytest.mark.parametrize(
    "message, color, glyph, number_str, number, indent_count, indent_char",
    [
        ("I am a test message", "white", None, None, None, 1, " "),
        ("I am a test message", "good", None, None, None, 1, " "),
        ("I am a test message", "bad", None, None, None, 1, " "),
        ("I am a test message2", "red", "🤣", " 1: ", 1, 1, " | "),
    ],
)
def test_console(message, color, glyph, number_str, number, indent_count, indent_char):
    console = ReciteConsole()
    console.print_message(
        message=message,
        color=color,
        glyph=glyph,
        number_str=number_str,
        indent_count=indent_count,
        indent_char=indent_char,
    )
    console.print_multiple_messages(
        messages=[message, message],
        color=color,
        indent_count=indent_count,
        indent_char=indent_char,
    )
    console.print_success(message=message, number=number)
    console.print_failure(message=message, number=number)
    console.print_error(message=message, indent_count=indent_count)
