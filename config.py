import json
import os
from pathlib import Path
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], config_path: str = "config.json"):
        self._defaults = defaults
        self._path = Path(config_path)
        self._data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not self._path.exists():
            return self._defaults.copy()
        try:
            with open(self._path, 'r') as f:
                user_data = json.load(f)
                return {**self._defaults, **user_data}
        except (json.JSONDecodeError, IOError):
            return self._defaults.copy()

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __repr__(self) -> str:
        return f"ConfigLoader(data={self._data})"

def get_config(defaults: Dict[str, Any], path: str = "config.json") -> ConfigLoader:
    return ConfigLoader(defaults, path)

# Usage example logic
if __name__ == "__main__":
    base_defaults = {"theme": "dark", "retries": 3, "verbose": False}
    cfg = get_config(base_defaults)
    print(f"Active configuration loaded: {cfg}")