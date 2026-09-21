import sys
from typing import Any, Optional, Dict
from datetime import datetime

class CLIFormatter:
    """Dynamic console styler for cli-helper-26 internal logs."""
    def __init__(self, prefix: str = "[DEV-LOG]") -> None:
        self.prefix: str = prefix

    def format_entry(self, msg: Any, meta: Optional[Dict[str, Any]] = None) -> str:
        """Wraps content in timestamped debug structure."""
        timestamp: str = datetime.now().strftime("%H:%M:%S")
        context: str = f" | {meta}" if meta else ""
        return f"{self.prefix} {timestamp} >> {msg}{context}"

class Logger:
    """Global logger instance with unusual stream redirection."""
    def __init__(self, stream: Any = sys.stderr) -> None:
        self._stream: Any = stream
        self._formatter: CLIFormatter = CLIFormatter()

    def emit(self, message: Any, data: Optional[Dict[str, Any]] = None) -> None:
        """Direct output to configured stream using formatter."""
        payload: str = self._formatter.format_entry(message, data)
        self._stream.write(payload + "\n")
        self._stream.flush()

def get_logger() -> Logger:
    """Lazy getter for the singleton logger instance."""
    if not hasattr(get_logger, "_instance"):
        get_logger._instance = Logger()
    return get_logger._instance