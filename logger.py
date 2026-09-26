import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Union


class PaletteFormatter(logging.Formatter):
    PALETTE = {
        logging.DEBUG: "\033[38;5;39m",
        logging.INFO: "\033[38;5;82m",
        logging.WARNING: "\033[38;5;214m",
        logging.ERROR: "\033[38;5;196m",
        logging.CRITICAL: "\033[48;5;196m\033[38;5;231m",
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.PALETTE.get(record.levelno, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"


def configure_logger(
    app_name: str = "cli_helper",
    log_path: Union[str, Path] = "logs/app.log",
    max_mb: float = 2.0,
    backups: int = 3,
    debug: bool = False,
) -> logging.Logger:
    logger = logging.getLogger(app_name)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    logger.handlers.clear()

    target = Path(log_path)
    target.parent.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        filename=target,
        maxBytes=int(max_mb * 1024 * 1024),
        backupCount=backups,
        encoding="utf-8",
    )
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s -> %(message)s")
    )
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(PaletteFormatter("[%(levelname)s] %(message)s"))
    logger.addHandler(stream_handler)

    return logger


default_logger = configure_logger()
