import functools
import os
import time
from typing import Callable, Any

def retry_operation(attempts: int = 3, delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def get_env_var(key: str, default: Any = None) -> str:
    val = os.environ.get(key, default)
    return str(val) if val is not None else ""

def flatten_list(nested: list) -> list:
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result

def smart_truncate(text: str, limit: int = 50) -> str:
    return (text[:limit] + '..') if len(text) > limit else text

def silent_execute(func: Callable, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception:
        return None