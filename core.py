import collections
from typing import Any, Iterable, Callable, Dict

class DataMorpher:
    """A whimsical transformer for nested structures."""
    def __init__(self, transforms: Dict[type, Callable[[Any], Any]] = None):
        self.transforms = transforms or {str: str.strip, int: abs}

    def process(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {str(k).lower(): self.process(v) for k, v in data.items()}
        elif isinstance(data, (list, tuple, set)):
            return [self.process(i) for i in data]
        elif type(data) in self.transforms:
            return self.transforms[type(data)](data)
        return data

def flatten_deep(structure: Iterable, depth: int = 1) -> list:
    """Recursive list flattening with depth constraint."""
    result = []
    for item in structure:
        if depth > 0 and isinstance(item, (list, tuple)):
            result.extend(flatten_deep(item, depth - 1))
        else:
            result.append(item)
    return result

def batch_process(data: Iterable, chunk_size: int = 5) -> Iterable:
    """Generator for chunking arbitrary iterables."""
    it = iter(data)
    while True:
        chunk = []
        try:
            for _ in range(chunk_size):
                chunk.append(next(it))
            yield chunk
        except StopIteration:
            if chunk:
                yield chunk
            break