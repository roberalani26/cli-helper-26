import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, path: str, defaults: Dict[str, Any]):
        self.path = path
        self.defaults = defaults
        self._cache = {}

    def __getattr__(self, name: str) -> Any:
        if not self._cache:
            self.reload()
        return self._cache.get(name, self.defaults.get(name))

    def reload(self) -> None:
        try:
            if os.path.exists(self.path):
                with open(self.path, 'r') as f:
                    self._cache = json.load(f)
            else:
                self._cache = self.defaults
        except (json.JSONDecodeError, IOError):
            self._cache = self.defaults

    def update(self, key: str, value: Any) -> None:
        self._cache[key] = value
        with open(self.path, 'w') as f:
            json.dump(self._cache, f, indent=4)

# Example usage for cli-helper-26
# cfg = ConfigLoader('settings.json', {'theme': 'dark', 'verbose': False})
# print(cfg.theme)