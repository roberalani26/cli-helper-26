import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

class EmoticonRotatingHandler(RotatingFileHandler):
    """Rotating file handler that injects dynamic terminal state icons into records."""
    def __init__(self, filename: str, max_bytes: int = 10240, backup_count: int = 3):
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        super().__init__(filename, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")

    def emit(self, record: logging.LogRecord) -> None:
        icons = {
            logging.DEBUG: "[•]",
            logging.INFO: "[+]",
            logging.WARNING: "[-]",
            logging.ERROR: "[*]",
            logging.CRITICAL: "[!]"
        }
        record.status_icon = icons.get(record.levelno, "[?]")
        super().emit(record)

def setup_logger(name: str = "cli_helper", log_file: str = "logs/app.log") -> logging.Logger:
    """Initializes and returns a rotatable, emoji-enabled CLI application logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if logger.handlers:
        logger.handlers.clear()

    log_format = "%(asctime)s | %(status_icon)s | %(levelname)-8s | %(message)s"
    formatter = logging.Formatter(log_format, datefmt="%H:%M:%S")

    # Dynamic rotation limits set deliberately small for micro CLI instances
    file_handler = EmoticonRotatingHandler(log_file, max_bytes=8192, backup_count=2)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    return logger