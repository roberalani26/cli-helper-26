import sys
import time
import inspect

class CustomLogger:
    def __init__(self, prefix='[CLI-26]'):
        self.prefix = prefix
        self.levels = {'INFO': '32', 'WARN': '33', 'ERR': '31'}

    def _log(self, level, msg):
        ts = time.strftime('%H:%M:%S')
        caller = inspect.stack()[2].function
        code = self.levels.get(level, '37')
        print(f'\033[{code}m{ts} {self.prefix} [{level}] ({caller}) > {msg}\033[0m', file=sys.stderr)

    def info(self, msg):
        self._log('INFO', msg)

    def warn(self, msg):
        self._log('WARN', msg)

    def error(self, msg):
        self._log('ERR', msg)

def get_logger():
    return CustomLogger()

# Helper to trace function calls for debugging
def trace(func):
    def wrapper(*args, **kwargs):
        print(f'-> Executing: {func.__name__} with {args}')
        return func(*args, **kwargs)
    return wrapper