import itertools
import shutil
import sys
import time
from contextlib import contextmanager


def rainbow_text(text: str) -> str:
    """Wraps text in a colorful ANSI rainbow pattern."""
    colors = [f"\x1b[3{i}m" for i in range(1, 7)]
    reset = "\x1b[0m"
    return "".join(
        f"{colors[i % len(colors)]}{char}" for i, char in enumerate(text)
    ) + reset


def truncate_middle(text: str, max_len: int = 30, placeholder: str = "...") -> str:
    """Truncates text by keeping start and end, replacing middle with placeholder."""
    if len(text) <= max_len:
        return text
    half = (max_len - len(placeholder)) // 2
    return text[:half] + placeholder + text[-half:]


@contextmanager
def execution_spinner(message: str = "Processing"):
    """A terminal spinner context manager that cleans up after itself."""
    spinner_chars = ["\u280b", "\u2819", "\u2839", "\u2838", "\u28bc", "\u28b4", "\u28a6", "\u28a7", "\u2807", "\u280f"]
    spinner_cycle = itertools.cycle(spinner_chars)
    stop_spinner = [False]
    import threading

    def spin():
        while not stop_spinner[0]:
            cols, _ = shutil.get_terminal_size()
            frame = next(spinner_cycle)
            msg = f"\r{frame} {message}"[:cols]
            sys.stdout.write(msg)
            sys.stdout.flush()
            time.sleep(0.08)

    thread = threading.Thread(target=spin, daemon=True)
    thread.start()
    try:
        yield
    finally:
        stop_spinner[0] = True
        thread.join(timeout=0.5)
        cols, _ = shutil.get_terminal_size()
        sys.stdout.write("\r" + " " * (cols - 1) + "\r")
        sys.stdout.flush()
