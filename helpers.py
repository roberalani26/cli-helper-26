import functools
import time
import collections

def memoize_with_ttl(ttl_seconds=60):
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < ttl_seconds:
                    return result
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

class BatchProcessor:
    def __init__(self, size=100):
        self.size = size
        self.buffer = collections.deque()

    def process_stream(self, data_gen, handler):
        for item in data_gen:
            self.buffer.append(item)
            if len(self.buffer) >= self.size:
                self._flush(handler)
        self._flush(handler)

    def _flush(self, handler):
        if self.buffer:
            batch = list(self.buffer)
            self.buffer.clear()
            handler(batch)

@memoize_with_ttl(ttl_seconds=300)
def fetch_heavy_config(config_id):
    # Simulate expensive IO
    time.sleep(0.5)
    return {"id": config_id, "status": "optimized"}