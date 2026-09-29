import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any] = None):
        self._data = defaults or {}

    def load_from_json(self, path: str) -> None:
        if os.path.exists(path):
            with open(path, 'r') as f:
                file_data = json.load(f)
                self._data.update(file_data)

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f'config key {name} missing')

    def __getitem__(self, key: str) -> Any:
        return self._data.get(key)

    def __repr__(self) -> str:
        return f"ConfigLoader({self._data})"

def get_config(path: str = 'config.json', defaults: Dict = None):
    loader = ConfigLoader(defaults)
    loader.load_from_json(path)
    
    class ConfigProxy:
        def __init__(self, d):
            self.__dict__ = d
            
    return ConfigProxy(loader._data)