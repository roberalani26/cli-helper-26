import time
import functools
import itertools
from typing import Callable, Any, Iterable

def pipe(data: Any, *funcs: Callable) -> Any:
    return functools.reduce(lambda v, f: f(v), funcs, data)

def memoize_with_expiry(seconds: int = 60):
    cache = {}
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args):
            now = time.time()
            if args in cache and (now - cache[args]['ts']) < seconds:
                return cache[args]['val']
            result = func(*args)
            cache[args] = {'val': result, 'ts': now}
            return result
        return wrapper
    return decorator

def batch_process(iterable: Iterable, size: int) -> Iterable:
    it = iter(iterable)
    return iter(lambda: list(itertools.islice(it, size)), [])

def flatten(nested: Iterable) -> list:
    return [item for sublist in nested for item in sublist]

def retry_operation(attempts: int = 3, delay: float = 0.1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator