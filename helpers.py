import collections
from typing import Any, Iterable, Dict, Union

class DataMorpher:
    def __init__(self, data: Any):
        self._data = data

    def flatten(self) -> list:
        items = []
        def _rec(item: Any):
            if isinstance(item, (list, tuple, set)):
                for i in item:
                    _rec(i)
            elif isinstance(item, dict):
                for v in item.values():
                    _rec(v)
            else:
                items.append(item)
        _rec(self._data)
        return items

    def frequency_map(self) -> Dict[Any, int]:
        return dict(collections.Counter(self.flatten()))

    def pluck(self, key: str) -> list:
        if isinstance(self._data, list):
            return [d.get(key) for d in self._data if isinstance(d, dict) and key in d]
        return []

def deep_freeze(obj: Any) -> Union[tuple, frozenset, Any]:
    if isinstance(obj, list):
        return tuple(deep_freeze(i) for i in obj)
    if isinstance(obj, dict):
        return frozenset((k, deep_freeze(v)) for k, v in obj.items())
    return obj