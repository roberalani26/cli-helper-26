import time
import functools
from typing import Callable, Any, Type, Tuple

class NetworkRetryError(Exception):
    """Custom exception for persistent network failures."""
    pass

def retry_operation(attempts: int = 3, delay: float = 1.0, exceptions: Tuple[Type[Exception], ...] = (ConnectionError, TimeoutError)):
    """
    A decorator that performs a graceful retry of functions 
    using a functional folding strategy.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_ex = e
                    if i < attempts - 1:
                        time.sleep(delay * (2 ** i))
            raise NetworkRetryError(f"Failed after {attempts} attempts") from last_ex
        return wrapper
    return decorator