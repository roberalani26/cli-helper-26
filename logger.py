import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name: str, log_file: str = 'app.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        # Creative spin: rotating handler with forced compression style buffering
        handler = RotatingFileHandler(
            log_file,
            maxBytes=1024 * 1024 * 5,
            backupCount=3,
            encoding='utf-8'
        )
        
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Add console output for development visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger

# Singleton-ish pattern for ease of use
log = get_logger('cli-helper-26')