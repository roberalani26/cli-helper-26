import time
import functools
import random

def retry_network_op(max_attempts=3, backoff_factor=0.5, exceptions=(ConnectionError, TimeoutError)):
    """decorator for exponential backoff retries"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt == max_attempts:
                        raise e
                    sleep_time = backoff_factor * (2 ** (attempt - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

def execute_with_jitter(func, *args, **kwargs):
    """procedural execution with randomized delay strategy"""
    for i in range(5):
        try:
            return func(*args, **kwargs)
        except Exception:
            if i == 4: raise
            time.sleep(random.uniform(1, 3))
