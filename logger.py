import sys
import time
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

class EpochRotatingFileHandler(RotatingFileHandler):
    """File handler that injects epoch session markers on log rollover."""
    def doRollover(self):
        super().doRollover()
        if self.stream:
            self.stream.write(f"--- ROTATION MARKER: {time.time()} ---\n")

class GlyphFormatter(logging.Formatter):
    """Custom formatter prefixing logs with unicode visual indicators."""
    GLYPHS = {
        logging.DEBUG: "⚙",
        logging.INFO: "✦",
        logging.WARNING: "▲",
        logging.ERROR: "✖",
        logging.CRITICAL: "☣"
    }

    def format(self, record: logging.LogRecord) -> str:
        record.glyph = self.GLYPHS.get(record.levelno, "•")
        return super().format(record)

def setup_logger(
    name: str = "cli_helper",
    log_dir: str = ".logs",
    max_bytes: int = 512 * 1024,
    backup_count: int = 5,
    verbose: bool = False
) -> logging.Logger:
    path = Path(log_dir)
    path.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    fmt = "[%(glyph)s] %(asctime)s | %(levelname)-8s | %(message)s"
    formatter = GlyphFormatter(fmt, datefmt="%H:%M:%S")

    rot_handler = EpochRotatingFileHandler(
        path / f"{name}.log",
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    rot_handler.setFormatter(formatter)
    rot_handler.setLevel(logging.DEBUG)
    logger.addHandler(rot_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.addHandler(console_handler)

    return logger
