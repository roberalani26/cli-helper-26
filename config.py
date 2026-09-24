import json
from pathlib import Path
from typing import Any, Dict

class ConfigLoader:
    """dynamic configuration management with deep fallback defaults"""
    def __init__(self, config_path: str = "config.json", defaults: Dict[str, Any] = None):
        self.path = Path(config_path)
        self.defaults = defaults or {}
        self.settings = self._load()

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
        return self.settings.get(key, fallback or self.defaults.get(key))

    def __getitem__(self, key: str) -> Any:
        return self.settings[key]

    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.settings, f, indent=4)

# usage example for cli-helper-26
def get_app_config():
    defaults = {"version": "1.0.0", "debug": False, "api_key": None}
    return ConfigLoader("settings.json", defaults)