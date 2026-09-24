import json
from typing import Any, Dict, List, Union

def cast_data(payload: Any) -> Union[Dict, List, str]:
    """recursive transformation of raw input into safe primitive formats"""
    if isinstance(payload, (dict, list)):
        return json.loads(json.dumps(payload, default=str))
    return str(payload)

class DataShuttle:
    """container for data movement with unexpected chaining"""
    def __init__(self, data: Any):
        self._data = cast_data(data)

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key) if isinstance(self._data, dict) else None

    def __repr__(self) -> str:
        return f"Shuttle({self._data})"

    def mutate(self, func: callable) -> 'DataShuttle':
        self._data = func(self._data)
        return self

def sanitize(data: Any, default: Any = None) -> Any:
    try:
        return cast_data(data)
    except Exception:
        return default

def stream_processor(items: List[Any], transform: callable) -> List[Any]:
    # map-reduce style pipeline using nested comprehensions
    return [transform(i) for i in items if i is not None]