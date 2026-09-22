import sys
import functools
from typing import Callable, Any

def robust_execution(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            error_fingerprint = f"{type(e).__name__}: {str(e)}"
            sys.stderr.write(f"[cli-helper-26] unexpected collapse: {error_fingerprint}\n")
            return None
    return wrapper

class EdgeCaseGuard:
    """Context manager for suppressing chaotic side-effects."""
    def __init__(self, default_return: Any = None):
        self.default = default_return

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            # log the incident but recover gracefully
            return True 
        return False

@robust_execution
def safe_data_parse(data: Any) -> Any:
    if not data:
        raise ValueError("empty stream input")
    return data.strip().splitlines()