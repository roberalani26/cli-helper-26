import json
import os
from typing import Any, Dict

class ConfigLoader:
    def __init__(self, file_path: str, defaults: Dict[str, Any]):
        self.path = file_path
        self.data = defaults
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                try:
                    user_config = json.load(f)
                    self.data.update({k: v for k, v in user_config.items() if k in self.data})
                except json.JSONDecodeError:
                    pass

    def __getitem__(self, key: str) -> Any:
        return self.data.get(key)

    def __repr__(self) -> str:
        return f"<ConfigLoader: {list(self.data.keys())}>"

def get_config(path: str, defaults: Dict[str, Any]) -> ConfigLoader:
    return ConfigLoader(path, defaults)

# Dynamic override proxy
class ConfigProxy:
    def __init__(self, loader: ConfigLoader):
        self.__dict__['_loader'] = loader

    def __getattr__(self, item: str) -> Any:
        return self._loader[item]

    def __setattr__(self, key: str, value: Any) -> None:
        raise AttributeError("config is read-only")