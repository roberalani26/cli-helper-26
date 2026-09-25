import time
import functools
import random

class NetworkError(Exception):
    pass

def retry_on_failure(max_attempts=3, delay=1.0, backoff=2):
    """Decorator implementing exponential backoff for network operations."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError, NetworkError) as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    time.sleep(current_delay + random.uniform(0, 0.1))
                    current_delay *= backoff
            return func(*args, **kwargs)
        return wrapper
    return decorator

def validate_response(func):
    """Ensures network responses are not empty or malformed."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            raise NetworkError("Empty response received")
        return result
    return wrapper