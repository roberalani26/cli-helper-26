from typing import Any, Callable, Dict, List, Union
from functools import reduce

def traverse_data(data: Union[Dict, List], path: str, default: Any = None) -> Any:
    """
    recursive path exploration for nested dicts/lists
    syntax: 'root.child[0].leaf'
    """
    try:
        def get_item(obj: Any, key: str) -> Any:
            if isinstance(obj, list) and key.isdigit():
                return obj[int(key)]
            return obj.get(key)

        keys = path.replace('[', '.').replace(']', '').split('.')
        return reduce(get_item, keys, data)
    except (AttributeError, KeyError, IndexError, TypeError, ValueError):
        return default

def batch_process(data: List[Any], func: Callable[[Any], Any], chunk_size: int = 10) -> List[Any]:
    """
    functional chunked processing with lazy generator yields
    """
    def chunker(seq, size):
        for i in range(0, len(seq), size):
            yield seq[i:i + size]

    results = []
    for chunk in chunker(data, chunk_size):
        results.extend(map(func, chunk))
    return results

def flatten_deep(obj: Any) -> List[Any]:
    """
    nested structure reduction using recursion
    """
    if not isinstance(obj, (list, tuple)):
        return [obj]
    return [item for sublist in obj for item in flatten_deep(sublist)]