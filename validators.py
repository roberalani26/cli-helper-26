import time
import functools
from typing import Callable, Any

def retry_operation(attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if i < attempts - 1:
                        time.sleep(current_delay)
                        current_delay *= backoff
            raise last_exception
        return wrapper
    return decorator

class NetworkValidator:
    def __init__(self, target: str):
        self.target = target

    @retry_operation(attempts=4, delay=0.5)
    def check_connectivity(self) -> bool:
        # simulate network ping
        import random
        if random.random() < 0.7:
            raise ConnectionError(f"ping failed for {self.target}")
        return True