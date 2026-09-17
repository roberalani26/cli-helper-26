import gzip
import logging
import os
import shutil
from logging.handlers import RotatingFileHandler
from pathlib import Path


class CompressedRotatingFileHandler(RotatingFileHandler):
    """Custom handler that automatically gzips log files upon rotation."""

    def __init__(self, filename: str | Path, maxBytes: int = 1_048_576, backupCount: int = 5, encoding: str = "utf-8"):
        super().__init__(filename, maxBytes=maxBytes, backupCount=backupCount, encoding=encoding)
        self.rotator = self._gzip_rotator
        self.namer = self._gzip_namer

    @staticmethod
    def _gzip_rotator(source: str, dest: str) -> None:
        with open(source, "rb") as f_in:
            with gzip.open(dest, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        if os.path.exists(source):
            os.remove(source)

    @staticmethod
    def _gzip_namer(name: str) -> str:
        return f"{name}.gz"


class BadgeFormatter(logging.Formatter):
    """Injects visual severity badges into formatted log messages."""

    BADGES = {
        logging.DEBUG: "🔍 [DEBUG]",
        logging.INFO: "💡 [INFO]",
        logging.WARNING: "⚠️  [WARN]",
        logging.ERROR: "🚨 [ERROR]",
        logging.CRITICAL: "💥 [CRIT]",
    }

    def format(self, record: logging.LogRecord) -> str:
        record.levelname = self.BADGES.get(record.levelno, "[LOG]")
        return super().format(record)


def setup_logger(name: str = "cli_helper", log_dir: str = ".logs", max_bytes: int = 524_288, backups: int = 3) -> logging.Logger:
    """Configures a CLI logger with auto-compressing file rotation."""
    target_dir = Path(log_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if not logger.handlers:
        fmt = "%(asctime)s | %(levelname)-10s | %(name)s:%(lineno)d - %(message)s"
        formatter = BadgeFormatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")

        file_handler = CompressedRotatingFileHandler(
            filename=target_dir / f"{name}.log",
            maxBytes=max_bytes,
            backupCount=backups
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
