import time
import functools
import logging

logger = logging.getLogger(__name__)

def with_retry(retries=3, delay=1.5, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries - 1:
                        logger.error(f"Final attempt failed for {func.__name__}")
                        raise e
                    logger.warning(f"Attempt {attempt + 1} failed, retrying in {current_delay}s")
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

def pulse_check(endpoint, timeout=5):
    import requests
    try:
        return requests.get(endpoint, timeout=timeout).status_code == 200
    except Exception:
        return False

@with_retry(retries=4, delay=1)
def secure_fetch(url):
    import requests
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.content