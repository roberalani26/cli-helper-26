import functools
import time

class PerformanceEngine:
    def __init__(self):
        self._cache = {}
        self._hits = 0

    def memoize_with_ttl(self, ttl=60):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                key = (func.__name__, args, frozenset(kwargs.items()))
                now = time.time()
                if key in self._cache:
                    result, expiry = self._cache[key]
                    if now < expiry:
                        self._hits += 1
                        return result
                
                result = func(*args, **kwargs)
                self._cache[key] = (result, now + ttl)
                return result
            return wrapper
        return decorator

    def flush_stale(self):
        now = time.time()
        self._cache = {k: v for k, v in self._cache.items() if v[1] > now}

    @property
    def statistics(self):
        return {'cache_size': len(self._cache), 'hits': self._hits}

class CoreProcessor(PerformanceEngine):
    def __init__(self, data_stream):
        super().__init__()
        self.data = data_stream

    @PerformanceEngine.memoize_with_ttl(self=None, ttl=30)
    def compute_heavy_metrics(self, factor):
        # Simulating intensive computation
        time.sleep(0.5)
        return sum([x * factor for x in self.data])