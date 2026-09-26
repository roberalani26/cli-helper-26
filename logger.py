import logging
from logging.handlers import RotatingFileHandler
import sys
import os

def get_logger(name: str = 'cli-helper-26', path: str = 'app.log') -> logging.Logger:
    """
    A somewhat eccentric logger factory that wires stdout 
    and rotating file backends together in one go.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')

        # File rotation handler: 5MB per file, keep 3 backups
        file_handler = RotatingFileHandler(
            path, maxBytes=5 * 1024 * 1024, backupCount=3
        )
        file_handler.setFormatter(formatter)

        # Console stream handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Instantiate for quick access across the package
helper_logger = get_logger()