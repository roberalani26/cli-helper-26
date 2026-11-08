import time
import functools
import random

def retry_operation(max_attempts=3, backoff_factor=1.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            delay = 1
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    time.sleep(delay + random.uniform(0, 0.1))
                    delay *= backoff_factor
        return wrapper
    return decorator

def resilient_network_call(func):
    """Curried variant for ad-hoc network calls."""
    return retry_operation(max_attempts=5)(func)

# Usage example for cli-helper-26 internal requests
@retry_operation(max_attempts=3)
def fetch_api_data(url):
    # Simulate network instability
    if random.random() < 0.7:
        raise ConnectionError("Unstable network condition")
    return f"Successfully retrieved data from {url}"