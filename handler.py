import time
import functools
from pathlib import Path
import json

def retry_on_failure(max_retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_retries - 1: raise
                    time.sleep(delay)
        return wrapper
    return decorator

class AtomicFileProcessor:
    def __init__(self, target_path):
        self.path = Path(target_path)

    def write_json_safely(self, data):
        tmp = self.path.with_suffix('.tmp')
        with open(tmp, 'w') as f:
            json.dump(data, f, indent=2)
        tmp.replace(self.path)

    @staticmethod
    def batch_process(items, func, chunk_size=5):
        return [func(items[i:i + chunk_size]) for i in range(0, len(items), chunk_size)]

def time_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f'{func.__name__} took {time.perf_counter() - start:.4f}s')
        return result
    return wrapper