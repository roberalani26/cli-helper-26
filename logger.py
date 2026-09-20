import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


class DynamicRotator(RotatingFileHandler):
    """Rotating file handler that writes a header marker upon log file rollover."""

    def doRollover(self) -> None:
        super().doRollover()
        if self.stream:
            timestamp = logging.Formatter().formatTime(
                logging.LogRecord("", 0, "", 0, "", (), None)
            )
            self.stream.write(f"=== LOG SESSION ROTATED AT {timestamp} ===\n")
            self.stream.flush()


def setup_cli_logger(
    name: str = "cli_helper",
    log_file: Optional[Path] = None,
    max_bytes: int = 512 * 1024,
    backup_count: int = 3,
    level: int = logging.INFO,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()

    console_fmt = logging.Formatter("[%(levelname)s] %(message)s")
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_fmt)
    logger.addHandler(console_handler)

    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_fmt = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
        )
        file_handler = DynamicRotator(
            filename=log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(file_fmt)
        logger.addHandler(file_handler)

    return logger


app_logger = setup_cli_logger(log_file=Path(".logs/cli.log"))
