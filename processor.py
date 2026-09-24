import time
import functools
import random

def with_retry(max_attempts=3, backoff=1.0):
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
                    sleep_time = backoff * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class NetworkProcessor:
    def __init__(self, timeout=5):
        self.timeout = timeout

    @with_retry(max_attempts=4, backoff=0.5)
    def fetch_data(self, url):
        # Simulate flaky network behavior
        if random.random() < 0.7:
            raise ConnectionError(f"Failed to connect to {url}")
        return {"status": 200, "data": "payload_data"}

def process_network_batch(urls):
    processor = NetworkProcessor()
    results = {}
    for url in urls:
        try:
            results[url] = processor.fetch_data(url)
        except Exception as e:
            results[url] = str(e)
    return results