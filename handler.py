import functools
import time

class PerformanceHandler:
    """Advanced request memoization with TTL and frequency throttling."""
    def __init__(self, cache_size=128, ttl=60):
        self.cache = {}
        self.cache_size = cache_size
        self.ttl = ttl

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            now = time.time()
            
            if key in self.cache:
                result, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    return result
            
            if len(self.cache) >= self.cache_size:
                oldest = min(self.cache, key=lambda k: self.cache[k][1])
                del self.cache[oldest]
                
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            return result
        return wrapper

@PerformanceHandler(cache_size=256, ttl=300)
def process_heavy_payload(data):
    # Simulate intensive transformation
    return [item[::-1] for item in sorted(data)]

if __name__ == "__main__":
    data_input = ["apple", "banana", "cherry"]
    print(process_heavy_payload(data_input))