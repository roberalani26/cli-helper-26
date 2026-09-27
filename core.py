import json
from typing import Any, Callable, Dict, Union

class DataMorpher:
    def __init__(self, data: Any):
        self._data = data

    def apply(self, func: Callable[[Any], Any]) -> 'DataMorpher':
        return DataMorpher(func(self._data))

    def extract(self) -> Any:
        return self._data

    def serialize(self) -> str:
        return json.dumps(self._data, default=str)

def sanitize_input(data: Union[dict, list]) -> Dict:
    """
    recursive deep sanitization of keys and values
    transforming all non-string keys into strings
    """
    if isinstance(data, dict):
        return {str(k): sanitize_input(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_input(i) for i in data]
    return data

def batch_process(items: list, transformer: Callable, chunk_size: int = 10):
    """
    generator-based batch processing for large lists
    using slice notation for memory efficiency
    """
    for i in range(0, len(items), chunk_size):
        batch = items[i:i + chunk_size]
        yield [transformer(item) for item in batch]

if __name__ == "__main__":
    data = {1: "a", 2: "b"}
    sanitized = sanitize_input(data)
    print(f"Sanitized: {sanitized}")