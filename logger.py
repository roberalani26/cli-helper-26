import sys
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional, TextIO, Union


class LogLevel(Enum):
    """Supported severity levels mapped to ANSI color escape codes."""
    TRACE = (10, "\033[38;5;244m")
    INFO = (20, "\033[38;5;39m")
    SUCCESS = (25, "\033[38;5;82m")
    WARN = (30, "\033[38;5;214m")
    ERROR = (40, "\033[38;5;196m")

    def __init__(self, weight: int, ansi_code: str) -> None:
        self.weight = weight
        self.ansi_code = ansi_code


class PrismLogger:
    """A spectrum-aware CLI logger supporting operator syntax and color output.

    Attributes:
        threshold: Minimum severity level to emit.
        stream: Output stream destination (defaults to sys.stderr).
        prefix: Label prepended to every log payload line.
    """

    RESET_CODE: str = "\033[0m"

    def __init__(
        self,
        threshold: LogLevel = LogLevel.INFO,
        stream: Optional[TextIO] = None,
        prefix: str = "cli-helper"
    ) -> None:
        """Initialize logger with explicit stream destination and filter threshold."""
        self.threshold: LogLevel = threshold
        self.stream: TextIO = stream if stream is not None else sys.stderr
        self.prefix: str = prefix

    def _format_entry(self, level: LogLevel, message: str) -> str:
        """Format a single log payload into an ANSI-decorated string."""
        now: str = datetime.now(timezone.utc).strftime("%H:%M:%S.%f")[:-3]
        tag: str = f"[{self.prefix}:{level.name}]"
        return f"{level.ansi_code}{now} {tag:<18} {message}{self.RESET_CODE}\n"

    def emit(self, level: LogLevel, payload: Any) -> "PrismLogger":
        """Emit a formatted message if payload meets severity threshold.

        Args:
            level: Severity level of the message.
            payload: Any object convertible to string.

        Returns:
            Self instance for operational chaining.
        """
        if level.weight >= self.threshold.weight:
            formatted: str = self._format_entry(level, str(payload))
            self.stream.write(formatted)
            self.stream.flush()
        return self

    def __lshift__(self, payload: Union[str, tuple[LogLevel, Any]]) -> "PrismLogger":
        """Overloaded left-shift operator for stream-style logging syntax.

        Usage: logger << "info message" or logger << (LogLevel.ERROR, "failure")
        """
        if isinstance(payload, tuple) and len(payload) == 2 and isinstance(payload[0], LogLevel):
            return self.emit(payload[0], payload[1])
        return self.emit(LogLevel.INFO, payload)


default_logger: PrismLogger = PrismLogger()
