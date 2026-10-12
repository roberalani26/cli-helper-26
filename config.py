import json
import os
from collections import ChainMap
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigCascade(ChainMap):
    """Hierarchical configuration manager resolving env vars, user files, and defaults."""

    DEFAULT_SETTINGS = {
        "theme": "dark",
        "verbose": False,
        "timeout": 30,
        "format": "json",
        "retry_limit": 3,
    }

    def __init__(self, defaults: Optional[Dict[str, Any]] = None, prefix: str = "CLI_"):
        base_defaults = {**self.DEFAULT_SETTINGS, **(defaults or {})}
        self._file_layer: Dict[str, Any] = {}
        self.prefix = prefix
        super().__init__(self._file_layer, base_defaults)

    def load_from_json(self, path: str | Path) -> "ConfigCascade":
        file_path = Path(path)
        if file_path.is_file():
            with open(file_path, "r", encoding="utf-8") as stream:
                self._file_layer.update(json.load(stream))
        return self

    def __getitem__(self, key: str) -> Any:
        env_var = f"{self.prefix}{key.upper()}"
        if env_var in os.environ:
            raw = os.environ[env_var]
            if raw.lower() in ("true", "1", "yes"):
                return True
            if raw.lower() in ("false", "0", "no"):
                return False
            if raw.isdigit():
                return int(raw)
            return raw
        return super().__getitem__(key)

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"Configuration option '{name}' not found")


def load_config(path: Optional[str] = None, **overrides) -> ConfigCascade:
    cfg = ConfigCascade()
    if path:
        cfg.load_from_json(path)
    cfg._file_layer.update(overrides)
    return cfg
