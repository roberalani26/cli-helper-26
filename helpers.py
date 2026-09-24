import time
import functools
import random

def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while x <= retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        raise e
                    delay = (backoff_in_seconds * (2 ** x)) + random.uniform(0, 1)
                    time.sleep(delay)
                    x += 1
        return wrapper
    return decorator

def request_stub(data):
    if random.random() < 0.7:
        raise ConnectionError("transient network glitch")
    return f"success: {data}"

if __name__ == '__main__':
    robust_call = retry_with_backoff()(request_stub)
    print(robust_call("ping"))