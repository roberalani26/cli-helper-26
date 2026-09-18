import functools
from typing import Any, Callable, Dict, List, Union

class DataFlux:
    """A magical wrapper for dictionary transformation gymnastics."""
    def __init__(self, data: Dict[Any, Any]):
        self._data = data

    def morph(self, keys: List[str], func: Callable[[Any], Any]) -> 'DataFlux':
        for key in keys:
            if key in self._data:
                self._data[key] = func(self._data[key])
        return self)

    def extract(self, path: str, default: Any = None) -> Any:
        return functools.reduce(
            lambda d, k: d.get(k, {}) if isinstance(d, dict) else default,
            path.split('.'),
            self._data
        )

    @property
    def raw(self) -> Dict[Any, Any]:
        return self._data

def sanitize_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively strips whitespace from string values."""
    def _clean(val: Any) -> Any:
        if isinstance(val, str):
            return val.strip()
        if isinstance(val, dict):
            return {k: _clean(v) for k, v in val.items()}
        if isinstance(val, list):
            return [_clean(i) for i in val]
        return val
    return _clean(data)

def smart_cast(value: Any, target_type: type) -> Any:
    """Aggressive type conversion attempt with safe fallback."""
    try:
        return target_type(value)
    except (ValueError, TypeError):
        return None