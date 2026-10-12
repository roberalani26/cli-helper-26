import time
import functools
from typing import Callable, Any, Dict

def time_execution(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"[DEBUG] {func.__name__} executed in {time.perf_counter() - start:.4f}s")
        return result
    return wrapper

def memoize_with_expiry(ttl: int = 300):
    def decorator(func: Callable):
        cache: Dict[tuple, tuple] = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key in cache and now - cache[key][1] < ttl:
                return cache[key][0]
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

class ChainBuilder:
    def __init__(self, value: Any):
        self.value = value
    
    def pipe(self, func: Callable, *args, **kwargs) -> 'ChainBuilder':
        self.value = func(self.value, *args, **kwargs)
        return self
    
    def get(self) -> Any:
        return self.value

def flatten(nested: list) -> list:
    flat = []
    for item in nested:
        if isinstance(item, list):
            flat.extend(flatten(item))
        else:
            flat.append(item)
    return flat