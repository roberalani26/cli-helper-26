import sys
import time
from typing import Any, Dict


class CLIHelperLogger:
    """A creative, latency-aware terminal logger for cli-helper-26."""

    COLORS: Dict[str, str] = {
        "DEBUG": "\u001b[36m",
        "INFO": "\u001b[32m",
        "WARNING": "\u001b[33m",
        "ERROR": "\u001b[31m",
        "RESET": "\u001b[0m",
    }

    def __init__(self, name: str = "CLI"):
        self.name = name
        self.last_log_time = time.time()

    def _get_latency_indicator(self) -> str:
        now = time.time()
        elapsed = now - self.last_log_time
        self.last_log_time = now
        if elapsed < 0.1:
            return "⚡"
        elif elapsed < 1.0:
            return "⏱️"
        return "⏳"

    def log(self, level: str, message: str, **kwargs: Any) -> None:
        color = self.COLORS.get(level.upper(), self.COLORS["RESET"])
        reset = self.COLORS["RESET"]
        indicator = self._get_latency_indicator()
        timestamp = time.strftime("%H:%M:%S")

        extra_tags = " ".join(f"[{k}={v}]" for k, v in kwargs.items())
        tag_str = f" \u001b[90m{extra_tags}\u001b[0m" if extra_tags else ""

        output = (
            f"[{timestamp}] {indicator} {color}[{level:7}]"
            f"{reset} ({self.name}) -> {message}{tag_str}"
        )
        sys.stdout.write(output + "\n")
        sys.stdout.flush()

    def debug(self, msg: str, **kwargs: Any) -> None:
        self.log("DEBUG", msg, **kwargs)

    def info(self, msg: str, **kwargs: Any) -> None:
        self.log("INFO", msg, **kwargs)

    def warn(self, msg: str, **kwargs: Any) -> None:
        self.log("WARNING", msg, **kwargs)

    def error(self, msg: str, **kwargs: Any) -> None:
        self.log("ERROR", msg, **kwargs)


logger = CLIHelperLogger("CORE")
