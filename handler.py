import json
from typing import Any, Dict, Union
from functools import reduce

def traverse_deep(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """navigates nested structures using dot-notation keys"""
    try:
        return reduce(lambda d, k: d.get(k, {}), path.split('.'), data)
    except AttributeError:
        return default

class DataMorph:
    """fluid transformations for nested dictionary objects"""
    def __init__(self, payload: Union[dict, str]):
        self.data = json.loads(payload) if isinstance(payload, str) else payload

    def pluck(self, key_path: str) -> Any:
        return traverse_deep(self.data, key_path)

    def flatten(self, parent_key='', sep='_'):
        items = []
        for k, v in self.data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(DataMorph(v).flatten(new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def mutate(self, key_path: str, func: callable) -> 'DataMorph':
        keys = key_path.split('.')
        target = self.data
        for k in keys[:-1]:
            target = target.setdefault(k, {})
        target[keys[-1]] = func(target.get(keys[-1]))
        return self

    def export(self) -> str:
        return json.dumps(self.data)