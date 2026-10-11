import sys
import logging
from datetime import datetime

class CliLogger:
    _instances = {}

    def __new__(cls, name='cli-helper-26'):
        if name not in cls._instances:
            instance = super().__new__(cls)
            instance._setup(name)
            cls._instances[name] = instance
        return cls._instances[name]

    def _setup(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(formatter)
        self.logger.addHandler(sh)

    def info(self, msg):
        self.logger.info(f"{self._get_timestamp()} - {msg}")

    def error(self, msg):
        self.logger.error(f"{self._get_timestamp()} - {msg}")

    @staticmethod
    def _get_timestamp():
        return datetime.now().strftime("%H:%M:%S")

def get_logger(name='cli-helper-26'):
    return CliLogger(name)