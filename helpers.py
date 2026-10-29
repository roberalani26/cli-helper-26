import time
import functools
import random

def retry(max_attempts=3, backoff_factor=1.0):
    """Decorator applying exponential backoff to network functions."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    sleep_time = (backoff_factor * (2 ** (attempts - 1))) + (random.uniform(0, 0.1))
                    time.sleep(sleep_time)
        return wrapper
    return decorator

def perform_network_call(func, *args, **kwargs):
    """Functional alternative to the retry decorator."""
    retry_wrapper = retry(max_attempts=3)(func)
    return retry_wrapper(*args, **kwargs)