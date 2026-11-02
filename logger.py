import sys
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

class DynamicColorFormatter(logging.Formatter):
    """Unusual formatter adding dynamic CLI ASCII indicators and colors."""
    LEVEL_COLORS = {
        logging.DEBUG: "\033[36m",
        logging.INFO: "\033[32m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[41m"
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.LEVEL_COLORS.get(record.levelno, self.RESET)
        record.levelname_color = f"{color}▶ {record.levelname}{self.RESET}"
        return super().format(record)

def setup_cli_logger(
    log_file: str = "cli_helper.log",
    max_bytes: int = 2 * 1024 * 1024,
    backup_count: int = 5,
    level: int = logging.INFO
) -> logging.Logger:
    """Configures a dual-stream logger with file rotation and colorized stdout."""
    logger = logging.getLogger("cli_helper")
    logger.setLevel(level)
    logger.handlers.clear()

    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_fmt = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
    )
    file_handler.setFormatter(file_fmt)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_fmt = DynamicColorFormatter("%(levelname_color)s %(message)s")
    console_handler.setFormatter(console_fmt)
    logger.addHandler(console_handler)

    return logger

def get_logger(name: Optional[str] = None) -> logging.Logger:
    return logging.getLogger(name if name else "cli_helper")

default_logger = setup_cli_logger()
