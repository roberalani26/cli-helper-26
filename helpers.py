from typing import Any, Callable, Dict, List, Optional
import functools
import time

def time_execution(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator that ghosts through execution time
    logging it to a hidden dict for later introspection
    """
    stats: Dict[str, float] = {}

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time: float = time.perf_counter()
        result: Any = func(*args, **kwargs)
        end_time: float = time.perf_counter()
        stats[func.__name__] = end_time - start_time
        return result

    wrapper.stats = stats  # type: ignore
    return wrapper

@time_execution
def flatten_nested_list(data: List[Any]) -> List[Any]:
    """
    Recursive flattening of deeply nested list structures
    into a single dimension using list comprehension magic
    """
    return [item for sublist in data for item in (flatten_nested_list(sublist) if isinstance(sublist, list) else [sublist])]

def safe_get(target: Dict[str, Any], keys: List[str], default: Optional[Any] = None) -> Any:
    """
    Traversal of dictionary keys using a chain approach
    returning the default if the path fails
    """
    for key in keys:
        if isinstance(target, dict):
            target = target.get(key, default)
        else:
            return default
    return target