"""CLI output layout and text formatting utilities."""

import sys
from typing import Any, Callable, Dict, List, Optional, Sequence, TypeVar

T = TypeVar("T")
FormatterFunc = Callable[[str], str]


class TerminalCanvas:
    """An unconventional stream decorator for styled CLI frame rendering."""

    def __init__(self, border_char: str = "│", width: int = 60) -> None:
        """Initialize canvas with custom border character and fixed width."""
        self.border_char: str = border_char
        self.width: int = width
        self._styles: Dict[str, FormatterFunc] = {
            "bold": lambda s: f"\033[1m{s}\033[0m",
            "dim": lambda s: f"\033[2m{s}\033[0m",
            "alert": lambda s: f"\033[31m{s}\033[0m",
        }

    def register_style(self, name: str, fn: FormatterFunc) -> "TerminalCanvas":
        """Register a dynamic text transformation callback to the style registry."""
        self._styles[name] = fn
        return self

    def frame_line(self, text: str, style: Optional[str] = None) -> str:
        """Wrap text into a padded canvas row with optional ANSI styling applied."""
        styled_text: str = (
            self._styles[style](text)
            if style and style in self._styles
            else text
        )
        padding: int = max(0, self.width - len(text) - 4)
        return f"{self.border_char} {styled_text}{' ' * padding} {self.border_char}"

    def render_block(
        self, items: Sequence[Any], transform: Optional[Callable[[Any], str]] = None
    ) -> List[str]:
        """Convert a sequence of items into a framed block of formatted lines."""
        converter: Callable[[Any], str] = transform or (lambda x: str(x))
        top: str = "+" + "-" * (self.width - 2) + "+"
        rows: List[str] = [top]
        for item in items:
            raw_val: str = converter(item)
            rows.append(self.frame_line(raw_val[: self.width - 4]))
        rows.append(top)
        return rows


def compose_transforms(
    *funcs: Callable[[T], T]
) -> Callable[[T], T]:
    """Chain multiple unary data transformers into a single functional pipeline."""

    def inner(val: T) -> T:
        res: T = val
        for f in funcs:
            res = f(res)
        return res

    return inner
