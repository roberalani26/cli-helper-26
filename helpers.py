import json
import os
from typing import Any, Dict

class ConfigLoader:
    """Dynamic configuration loader with fallback defaults."""
    def __init__(self, defaults: Dict[str, Any]):
        self._data = defaults.copy()

    def load_from_json(self, path: str) -> None:
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    self._data.update(json.load(f))
        except (json.JSONDecodeError, IOError):
            pass

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"config has no attribute {name}")

def load_config(file_path: str, defaults: Dict[str, Any]) -> ConfigLoader:
    loader = ConfigLoader(defaults)
    loader.load_from_json(file_path)
    return loader