import json
import os
from pathlib import Path
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str, defaults: Dict[str, Any] = None):
        self.path = Path(path)
        self.defaults = defaults or {}
        self._data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self.path.exists():
            return self.defaults
        try:
            with open(self.path, 'r') as f:
                loaded = json.load(f)
                return {**self.defaults, **loaded}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def get(self, key: str, fallback: Any = None) -> Any:
        return self._data.get(key, fallback)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def persist(self) -> None:
        with open(self.path, 'w') as f:
            json.dump(self._data, f, indent=4)

def load_config(filename: str = 'config.json') -> ConfigLoader:
    default_map = {'version': '1.0.0', 'debug': False}
    return ConfigLoader(filename, default_map)