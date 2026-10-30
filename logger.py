import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Callable, Any

class DynamicColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[36m",
        logging.INFO: "\033[32m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[41m",
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, self.RESET)
        record.levelname = f"{color}{record.levelname:<8}{self.RESET}"
        return super().format(record)

def setup_rotating_logger(
    name: str = "cli_helper",
    log_file: Optional[str] = None,
    max_bytes: int = 1_048_576,
    backup_count: int = 5,
    level: int = logging.INFO
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(DynamicColorFormatter("[%(asctime)s] %(levelname)s %(message)s", "%H:%M:%S"))
    logger.addHandler(console)

    if not log_file:
        log_dir = Path.home() / ".cli_helper" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = str(log_dir / "app.log")

    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger

def trace_execution(logger: logging.Logger) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.debug(f"Entering {func.__name__} with args={args}, kwargs={kwargs}")
            try:
                res = func(*args, **kwargs)
                logger.debug(f"Exited {func.__name__} successfully")
                return res
            except Exception as exc:
                logger.error(f"Failed in {func.__name__}: {exc}", exc_info=True)
                raise
        return wrapper
    return decorator
