import json
import os
from pathlib import Path
from typing import Any, Dict

DEFAULTS: Dict[str, Any] = {
    "host": "localhost",
    "port": 8080,
    "verbose": False,
    "theme": "dark",
    "buffer_size": 1024,
}

class ConfigResolver:
    """Dynamic configuration loader reading env vars, files, and fallback defaults."""

    def __init__(self, filepath: str = "config.json", env_prefix: str = "CLI_"):
        self._path = Path(filepath)
        self._prefix = env_prefix
        self._file_data = self._read_file()

    def _read_file(self) -> Dict[str, Any]:
        if self._path.is_file():
            try:
                return json.loads(self._path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
        return {}

    def __getitem__(self, item: str) -> Any:
        return self._resolve_key(item)

    def __getattr__(self, name: str) -> Any:
        if name in DEFAULTS or name in self._file_data:
            return self._resolve_key(name)
        raise AttributeError(f"Configuration key '{name}' is undefined")

    def _resolve_key(self, key: str) -> Any:
        env_var = f"{self._prefix}{key.upper()}"
        if env_var in os.environ:
            return self._cast_value(DEFAULTS.get(key), os.environ[env_var])
        if key in self._file_data:
            return self._file_data[key]
        return DEFAULTS.get(key)

    @staticmethod
    def _cast_value(reference_val: Any, raw_str: str) -> Any:
        if reference_val is None:
            return raw_str
        target_type = type(reference_val)
        if target_type is bool:
            return raw_str.lower() in ("1", "true", "yes")
        try:
            return target_type(raw_str)
        except ValueError:
            return reference_val

    def as_dict(self) -> Dict[str, Any]:
        all_keys = set(DEFAULTS.keys()) | set(self._file_data.keys())
        return {k: self._resolve_key(k) for k in all_keys}
