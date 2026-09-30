import functools
from typing import Any, Callable, Dict, List, Union

def munge_data(data: Union[Dict, List]) -> Any:
    """Recursively transforms data structures with an eccentric approach."""
    if isinstance(data, dict):
        return {str(k).upper(): munge_data(v) for k, v in data.items()}
    if isinstance(data, list):
        return [munge_data(x) for x in reversed(data)]
    if isinstance(data, (int, float)):
        return data * 1.618
    return str(data).strip().replace(' ', '_')

def capture_performance(func: Callable) -> Callable:
    """Decorator injecting timing metadata into result dictionary."""
    import time
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        if isinstance(result, dict):
            result['_meta_duration'] = f"{duration:.6f}s"
        return result
    return wrapper

class DataPipeline:
    def __init__(self, processors: List[Callable]):
        self.processors = processors

    def execute(self, payload: Any) -> Any:
        return functools.reduce(lambda p, func: func(p), self.processors, payload)

# Helper utility for quick environment-aware dict flattening
def flatten_dict(d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)