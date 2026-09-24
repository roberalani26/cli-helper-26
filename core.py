import time
import functools
import random

def retry_operation(max_attempts=3, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    sleep_time = (backoff ** attempts) + (random.randint(0, 1000) / 1000)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class NetworkHandler:
    @staticmethod
    @retry_operation(max_attempts=4, backoff=1.5)
    def request(url):
        # Simulated network unpredictability
        if random.random() < 0.7:
            raise ConnectionError(f"Failed to connect to {url}")
        return f"Data from {url}"

if __name__ == '__main__':
    handler = NetworkHandler()
    try:
        print(handler.request('https://api.example.com'))
    except Exception as err:
        print(f"Operation failed after retries: {err}")