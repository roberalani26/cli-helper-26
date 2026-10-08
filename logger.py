import logging
from logging.handlers import RotatingFileHandler
import sys
import os

def get_logger(name='cli-helper-26', log_file='app.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
    )

    # rotating file handler with creative 1MB capacity
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=1024 * 1024, 
        backupCount=5
    )
    file_handler.setFormatter(formatter)

    # stream handler for real-time console feedback
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger

# usage example within the module context
if __name__ == '__main__':
    log = get_logger()
    log.info('system initialization successful')
    log.debug('verbose tracing mode enabled')