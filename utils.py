import sys
import time
from functools import wraps
from typing import Any, Callable, Dict, Generic, ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")


class ColorPalette:
    """Dynamic ANSI terminal color injector using attribute lookup."""

    COLORS: Dict[str, str] = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "reset": "\033[0m",
    }

    def __getattr__(self, name: str) -> Callable[[str], str]:
        """Generates a text wrapping function for valid color names."""
        color_code = self.COLORS.get(name.lower())
        if not color_code:
            raise AttributeError(f"Palette has no color named '{name}'")

        def colorize(text: str) -> str:
            return f"{color_code}{text}{self.COLORS['reset']}"

        return colorize


palette: ColorPalette = ColorPalette()


class DynamicPipe(Generic[T]):
    """Monadic CLI text pipeline supporting chained transformations."""

    def __init__(self, value: T) -> None:
        """Initialize the pipeline with an arbitrary payload."""
        self._value: T = value

    def pipe(self, func: Callable[[T], Any]) -> "DynamicPipe[Any]":
        """Apply transformation function to contained value."""
        return DynamicPipe(func(self._value))

    def unwrap(self) -> T:
        """Extract final processed value from the pipe."""
        return self._value


def timed_spinner(label: str) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator adding dynamic stdout feedback ticks to wrapped execution."""

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            sys.stdout.write(f"{palette.cyan('[wait]')} {label}...")
            sys.stdout.flush()
            time.sleep(0.1)
            result = func(*args, **kwargs)
            sys.stdout.write(f"\r{palette.green('[ok]')}   {label}\n")
            return result

        return wrapper

    return decorator
