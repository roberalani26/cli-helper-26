import functools
from typing import Any, Callable, Iterable, Union

def pipe(data: Any, *funcs: Callable) -> Any:
    return functools.reduce(lambda v, f: f(v), funcs, data)

def sanitize(data: Any) -> Any:
    if isinstance(data, dict):
        return {str(k): sanitize(v) for k, v in data.items()}
    if isinstance(data, (list, tuple, set)):
        return [sanitize(i) for i in data]
    if data is None:
        return ""
    return data

def deep_flatten(items: Iterable) -> list:
    flat = []
    for item in items:
        if isinstance(item, (list, tuple)):
            flat.extend(deep_flatten(item))
        else:
            flat.append(item)
    return flat

def batch_process(data: list, size: int = 10) -> Iterable:
    for i in range(0, len(data), size):
        yield data[i:i + size]

def smart_transform(data: Any, transform_map: dict) -> Any:
    def _apply(val):
        for key, func in transform_map.items():
            if isinstance(val, key):
                return func(val)
        return val
    return _apply(data)