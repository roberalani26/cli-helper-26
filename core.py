import functools
import time

class PerformanceEngine:
    """Advanced memoization with TTL and size constraints."""
    def __init__(self, limit=1024, ttl=60):
        self.cache = {}
        self.limit = limit
        self.ttl = ttl

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key in self.cache:
                result, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    return result
            
            if len(self.cache) >= self.limit:
                oldest = min(self.cache, key=lambda k: self.cache[k][1])
                del self.cache[oldest]
            
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            return result
        return wrapper

engine = PerformanceEngine(limit=500)

@engine
def process_data(data_blob: str) -> int:
    # Simulate intensive computational task
    return sum(ord(c) for c in data_blob) * 42

def run_core_operations(input_data):
    return [process_data(i) for i in input_data]