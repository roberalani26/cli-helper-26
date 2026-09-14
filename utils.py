import time
import functools
import logging

logger = logging.getLogger(__name__)

def retry_operation(max_attempts=3, delay=1.0, backoff=2.0, exceptions=(Exception,)):
    """Decorator implementing exponential backoff for flaky operations."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts == max_attempts:
                        logger.error(f"Final attempt {attempts} failed: {e}")
                        raise
                    logger.warning(f"Attempt {attempts} failed. Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

class NetworkSession:
    def __init__(self):
        self.connected = False

    @retry_operation(max_attempts=3, delay=0.5)
    def request(self, endpoint):
        """Simulated volatile network request."""
        if not self.connected:
            self.connected = True
            raise ConnectionError("Initial connection drop")
        return {"status": 200, "data": f"success from {endpoint}"}