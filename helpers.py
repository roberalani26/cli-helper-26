import sys
import os
import time
from typing import Callable, Any, TypeVar

T = TypeVar("T")

class Pipe:
    """Unusual bitwise-pipe wrapper for CLI string manipulation chains."""
    def __init__(self, value: Any):
        self.value = str(value)

    def __or__(self, func: Callable[[str], str]) -> "Pipe":
        return Pipe(func(self.value))

    def __repr__(self) -> str:
        return self.value

    def emit(self, stream=sys.stdout) -> None:
        stream.write(self.value + "\n")

def ansi_style(fg: int = 37, bg: int = 40, bold: bool = False) -> Callable[[str], str]:
    style = f"\033[{1 if bold else 0};{fg};{bg}m"
    return lambda text: f"{style}{text}\033[0m"

def wrap_box(title: str = "") -> Callable[[str], str]:
    def _box(text: str) -> str:
        lines = text.splitlines() or [""]
        w = max(max((len(line) for line in lines), default=0), len(title) + 2)
        header = f"┌─ {title} ─{'─' * (w - len(title) - 4)}┐" if title else f"┌{'─' * (w + 2)}┐"
        footer = f"└{'─' * (w + 2)}┘"
        content = "\n".join(f"│ {line.ljust(w)} │" for line in lines)
        return f"{header}\n{content}\n{footer}"
    return _box

def clip_text(limit: int = 80, pad: str = "...") -> Callable[[str], str]:
    return lambda t: t if len(t) <= limit else t[:limit - len(pad)] + pad

def timed_run(action_name: str = "operation") -> Callable:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Any, **kwargs: Any) -> T:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = (time.perf_counter() - start) * 1000
            sys.stderr.write(f"[{action_name}] completed in {elapsed:.2f}ms\n")
            return result
        return wrapper
    return decorator
