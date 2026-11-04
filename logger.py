import datetime
from typing import Any, NoReturn

class CLIConsoleLogger:
    """Custom console logger with timestamped decoration."""

    def __init__(self, prefix: str = "[cli-helper-26]") -> None:
        self.prefix: str = prefix

    def log(self, message: Any) -> None:
        """Prints formatted message to stdout."""
        timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{self.prefix} {timestamp} | {str(message)}")

    def critical_error(self, message: str) -> NoReturn:
        """Logs a fatal message and triggers an exception."""
        self.log(f"CRITICAL: {message}")
        raise RuntimeError(f"Execution aborted: {message}")

def get_logger(module_name: str = "default") -> CLIConsoleLogger:
    """Factory function returning a configured logger instance."""
    return CLIConsoleLogger(prefix=f"[{module_name.upper()}]")

if __name__ == "__main__":
    logger: CLIConsoleLogger = get_logger("core")
    logger.log("system initialized successfully")