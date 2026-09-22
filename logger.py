import logging
from logging.handlers import RotatingFileHandler
import sys

class LoggerSetup:
    def __init__(self, name='cli-helper-26', log_file='app.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.setup_handlers(log_file)

    def setup_handlers(self, log_file):
        if not self.logger.handlers:
            file_handler = RotatingFileHandler(
                log_file, maxBytes=1048576, backupCount=5
            )
            file_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)

            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(self.formatter)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

def get_app_logger():
    return LoggerSetup().get_logger()

if __name__ == '__main__':
    log = get_app_logger()
    log.info('logger initialization successful')