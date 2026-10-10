import os
import json
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, defaults: Dict[str, Any], config_path: str = "config.json"):
        self.defaults = defaults
        self.path = config_path
        self._data = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return self.defaults
        try:
            with open(self.path, "r") as f:
                loaded = json.load(f)
                return {**self.defaults, **loaded}
        except (json.JSONDecodeError, IOError):
            return self.defaults

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Config has no attribute '{name}'")

    def save(self) -> None:
        with open(self.path, "w") as f:
            json.dump(self._data, f, indent=4)

def get_config(overrides: Dict[str, Any] = None) -> ConfigLoader:
    defaults = {
        "version": "1.0.0",
        "debug": False,
        "timeout": 30,
        "retries": 3
    }
    if overrides:
        defaults.update(overrides)
    return ConfigLoader(defaults)