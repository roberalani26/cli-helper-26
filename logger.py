import sys
from datetime import datetime
from typing import Any

class Colorizer:
    COLORS = {'info': '\033[94m', 'warn': '\033[93m', 'error': '\033[91m', 'reset': '\033[0m'}

    @classmethod
    def format(cls, level: str, msg: str) -> str:
        color = cls.COLORS.get(level.lower(), cls.COLORS['reset'])
        timestamp = datetime.now().strftime('%H:%M:%S')
        return f"{color}[{timestamp}] [{level.upper()}]{cls.COLORS['reset']} {msg}"

def log(level: str, message: Any) -> None:
    output = Colorizer.format(level, str(message))
    if level.lower() == 'error':
        print(output, file=sys.stderr)
    else:
        print(output)

class LoggerProxy:
    def __init__(self, prefix: str):
        self.prefix = prefix

    def info(self, msg: str): log('info', f"{self.prefix}: {msg}")
    def warn(self, msg: str): log('warn', f"{self.prefix}: {msg}")
    def error(self, msg: str): log('error', f"{self.prefix}: {msg}")

def get_logger(name: str) -> LoggerProxy:
    return LoggerProxy(name)