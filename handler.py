import functools
import collections
import time

class ExecutionEngine:
    def __init__(self):
        self._memo = {}
        self._hits = collections.deque(maxlen=1000)

    def fast_track(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            if key in self._memo:
                return self._memo[key]
            
            result = func(*args, **kwargs)
            
            if len(self._memo) > 1000:
                oldest = self._hits.popleft()
                self._memo.pop(oldest, None)
            
            self._memo[key] = result
            self._hits.append(key)
            return result
        return wrapper

    @staticmethod
    def batch_process(data, chunk_size=10):
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]

def optimize_compute(func):
    engine = ExecutionEngine()
    return engine.fast_track(func)

if __name__ == '__main__':
    @optimize_compute
    def heavy_calculation(n):
        time.sleep(0.1)
        return n * n

    start = time.perf_counter()
    [heavy_calculation(x) for x in range(5)]
    [heavy_calculation(x) for x in range(5)]
    print(f'Execution duration: {time.perf_counter() - start:.4f}s')