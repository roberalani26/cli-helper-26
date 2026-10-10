import sys
import shutil
from typing import Callable, Any


class TextPipe:
    """An operator-overloaded pipeline wrapper for CLI string transforms."""

    def __init__(self, value: str):
        self.value = str(value)

    def __or__(self, func: Callable[[str], str]) -> "TextPipe":
        return TextPipe(func(self.value))

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"TextPipe({self.value!r})"


def colorize(ansi_code: int) -> Callable[[str], str]:
    """Wrap text in standard ANSI color and style sequence."""
    return lambda text: f"\033[{ansi_code}m{text}\033[0m"


def truncate_to_term(padding: int = 4) -> Callable[[str], str]:
    """Truncate text dynamically to fit current terminal width."""
    def _inner(text: str) -> str:
        cols, _ = shutil.get_terminal_size(fallback=(80, 24))
        max_len = max(10, cols - padding)
        return text if len(text) <= max_len else text[: max_len - 3] + "..."
    return _inner


def center_pad(char: str = "─") -> Callable[[str], str]:
    """Center text inside a decorative horizontal bar."""
    def _inner(text: str) -> str:
        cols, _ = shutil.get_terminal_size(fallback=(80, 24))
        side_len = max(1, (cols - len(text) - 2) // 2)
        banner = char * side_len
        return f"{banner} {text} {banner}"
    return _inner


def wrap_kv(key: str) -> Callable[[Any], str]:
    """Format raw value into a styled key-value output entry."""
    def _inner(val: Any) -> str:
        key_tag = colorize(36)(f"[{key}]")
        return f"{key_tag} {val}"
    return _inner


def prompt_choice(options: list[str], default: str = "") -> str:
    """Interactively prompt user for choice with prefix matching."""
    opts_fmt = " / ".join(
        f"\033[1m{o}\033[0m" if o == default else o for o in options
    )
    sys.stdout.write(f"Select ({opts_fmt}): ")
    sys.stdout.flush()
    raw_input = sys.stdin.readline().strip().lower()
    if not raw_input and default:
        return default
    for opt in options:
        if opt.lower().startswith(raw_input):
            return opt
    return raw_input or default
