import time
import functools
from typing import Callable, Any

def retry_on_failure(retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator

def pipe(data: Any, *funcs: Callable):
    return functools.reduce(lambda v, f: f(v), funcs, data)

class FrozenDict(dict):
    def __setitem__(self, key, value):
        raise TypeError("immutable configuration dictionary")
    def __delitem__(self, key):
        raise TypeError("immutable configuration dictionary")

def batch_process(items: list, size: int):
    for i in range(0, len(items), size):
        yield items[i:i + size]

def smart_coalesce(*args):
    return next((arg for arg in args if arg is not None), None)