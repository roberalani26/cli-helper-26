import functools
import logging

class OptimizationError(Exception):
    """Custom exception for performance-related bottlenecks."""
    pass

def memoize_with_ttl(ttl=300):
    """Creative caching decorator to prevent redundant compute."""
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            if key in cache:
                return cache[key]
            result = func(*args, **kwargs)
            cache[key] = result
            return result
        return wrapper
    return decorator

def performance_monitor(threshold=0.5):
    """Decorator that tracks execution time of core functions."""
    import time
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            if elapsed > threshold:
                logging.warning(f"Performance degradation in {func.__name__}: {elapsed:.4f}s")
            return result
        return wrapper
    return decorator

class LazyLoader:
    """Delayed initialization for memory-heavy resources."""
    def __init__(self, factory):
        self._factory = factory
        self._instance = None

    @property
    def instance(self):
        if self._instance is None:
            self._instance = self._factory()
        return self._instance