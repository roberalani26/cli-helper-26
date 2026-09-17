import os
import math
from typing import Any, Dict, Callable

class EdgeCaseSanitizer:
    """Sanitizes edge-case inputs like infinity, recursive env vars, and byte corruption."""
    
    @staticmethod
    def resolve_env_cascade(key: str, default: Any, depth: int = 0) -> Any:
        if depth > 5:
            return default
        val = os.getenv(key)
        if val is None:
            return default
        if val.startswith("$") and val[1:] in os.environ:
            return EdgeCaseSanitizer.resolve_env_cascade(val[1:], default, depth + 1)
        return val

    @staticmethod
    def safe_cast(value: Any, target_type: type, fallback: Any) -> Any:
        try:
            if target_type is float:
                res = float(value)
                if math.isnan(res) or math.isinf(res):
                    return fallback
                return res
            if target_type is bool and isinstance(value, str):
                clean = value.strip().lower()
                if clean in ("true", "1", "yes", "on"):
                    return True
                if clean in ("false", "0", "no", "off"):
                    return False
                return fallback
            return target_type(value)
        except (ValueError, TypeError, OverflowError):
            return fallback

class ResilientConfig:
    def __init__(self, defaults: Dict[str, Any] = None):
        self._store: Dict[str, Any] = defaults or {"timeout": 30, "verbose": False, "rate_limit": 1.5}
        self._fallback_hooks: Dict[str, Callable[[], Any]] = {}

    def register_fallback(self, key: str, hook: Callable[[], Any]):
        self._fallback_hooks[key] = hook

    def get(self, key: str, expected_type: type = str) -> Any:
        raw_env = EdgeCaseSanitizer.resolve_env_cascade(key.upper(), None)
        if raw_env is not None:
            res = EdgeCaseSanitizer.safe_cast(raw_env, expected_type, None)
            if res is not None:
                return res

        if key in self._store:
            return EdgeCaseSanitizer.safe_cast(self._store[key], expected_type, None)

        if key in self._fallback_hooks:
            try:
                res = self._fallback_hooks[key]()
                return EdgeCaseSanitizer.safe_cast(res, expected_type, None)
            except Exception:
                pass

        return None