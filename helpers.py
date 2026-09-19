import sys
import logging
import datetime
from pathlib import Path
from logging.handlers import RotatingFileHandler

class RotatingANSIFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[36m",
        logging.INFO: "\033[32m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[41m"
    }
    RESET = "\033[0m"

    def __init__(self, use_color: bool = True):
        super().__init__(fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        self.use_color = use_color

    def format(self, record: logging.LogRecord) -> str:
        formatted = super().format(record)
        if self.use_color and record.levelno in self.COLORS:
            color = self.COLORS[record.levelno]
            return f"{color}{formatted}{self.RESET}"
        return formatted

class MetaHeaderRotatingHandler(RotatingFileHandler):
    def doRollover(self):
        super().doRollover()
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        if self.stream:
            self.stream.write(f"--- LOG SESSION ROTATED AT {timestamp} ---\n")
            self.stream.flush()

def setup_logger(
    name: str = "cli_app",
    log_file: str = "app.log",
    max_bytes: int = 1_048_576,
    backup_count: int = 5,
    level: int = logging.INFO
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()

    file_path = Path(log_file)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_handler = MetaHeaderRotatingHandler(
        file_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setFormatter(RotatingANSIFormatter(use_color=False))
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(RotatingANSIFormatter(use_color=True))
    logger.addHandler(console_handler)

    return logger