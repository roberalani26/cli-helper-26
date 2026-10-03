import json
from typing import Any, Callable, Dict, Optional

class DataTransformPipe:
    """A functional-style pipeline for data transformation chains."""
    def __init__(self, data: Any):
        self._data = data

    def apply(self, func: Callable[[Any], Any]) -> 'DataTransformPipe':
        self._data = func(self._data)
        return self

    def value(self) -> Any:
        return self._data

def cast_structure(data: Any, cast_map: Dict[str, type]) -> Dict[str, Any]:
    """Enforce dictionary schemas through key-based type mapping."""
    if not isinstance(data, dict):
        return {}
    return {k: cast_map.get(k, str)(v) for k, v in data.items() if k in cast_map}

def safe_json_load(payload: str, fallback: Any = None) -> Any:
    """Resilient JSON ingestion with silent failure defaults."""
    try:
        return json.loads(payload)
    except (json.JSONDecodeError, TypeError):
        return fallback

def recursive_map(func: Callable, target: Any) -> Any:
    """Deep recursive traversal for arbitrary data manipulation."""
    if isinstance(target, dict):
        return {k: recursive_map(func, v) for k, v in target.items()}
    if isinstance(target, list):
        return [recursive_map(func, i) for i in target]
    return func(target)