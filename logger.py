import functools
import time
import sys

class AsyncBufferLogger:
    def __init__(self, size_limit=100):
        self._buffer = []
        self._limit = size_limit

    def log(self, message):
        self._buffer.append(f'[{time.time():.4f}] {message}')
        if len(self._buffer) >= self._limit:
            self.flush()

    def flush(self):
        if self._buffer:
            sys.stdout.write('\n'.join(self._buffer) + '\n')
            self._buffer.clear()

def memoize_logger(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

class PerformanceLogger(AsyncBufferLogger):
    @memoize_logger
    def format_entry(self, level, msg):
        return f'{level.upper()} | {msg}'

    def info(self, msg):
        self.log(self.format_entry('info', msg))

logger = PerformanceLogger()