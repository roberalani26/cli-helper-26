import os
import json
from collections import ChainMap
from pathlib import Path
from typing import Any, Dict


class DynamicConfig:
    """Configuration loader using ChainMap with automatic type coercion and ENV fallback."""

    def __init__(self, default_config: Dict[str, Any], config_path: str | Path | None = None):
        self._defaults = default_config
        self._file_config = self._load_file(config_path) if config_path else {}
        self._env_prefix = "CLI_APP_"
        self._chain = ChainMap({}, self._file_config, self._defaults)

    def _load_file(self, path: str | Path) -> Dict[str, Any]:
        p = Path(path)
        if p.exists() and p.suffix.lower() == ".json":
            try:
                with p.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _coerce_env_value(self, val: str) -> Any:
        if val.lower() in ("true", "false"):
            return val.lower() == "true"
        try:
            return int(val)
        except ValueError:
            try:
                return float(val)
            except ValueError:
                return val

    def get(self, key: str, default: Any = None) -> Any:
        env_key = f"{self._env_prefix}{key.upper()}"
        if env_key in os.environ:
            return self._coerce_env_value(os.environ[env_key])
        return self._chain.get(key, default)

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(f"No attribute {name}")
        val = self.get(name)
        if val is None:
            raise AttributeError(f"Configuration key '{name}' not found")
        return val

    def as_dict(self) -> Dict[str, Any]:
        env_overrides = {
            k[len(self._env_prefix):].lower(): self._coerce_env_value(v)
            for k, v in os.environ.items()
            if k.startswith(self._env_prefix)
        }
        return dict(ChainMap(env_overrides, self._file_config, self._defaults))


DEFAULT_SETTINGS = {
    "theme": "dark",
    "timeout": 30,
    "verbose": False,
    "max_retries": 3,
    "output_format": "json"
}

cfg = DynamicConfig(DEFAULT_SETTINGS)
