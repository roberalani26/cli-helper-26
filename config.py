import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str = 'config.json', defaults: Dict[str, Any] = None):
        self.path = path
        self.defaults = defaults or {}
        self.data = self._load_recursive(self.defaults)

    def _load_recursive(self, base: Dict[str, Any]) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return base
        try:
            with open(self.path, 'r') as f:
                loaded = json.load(f)
            return {**base, **loaded}
        except (json.JSONDecodeError, IOError):
            return base

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def persist(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def __repr__(self):
        return f"<ConfigLoader keys={list(self.data.keys())}>"