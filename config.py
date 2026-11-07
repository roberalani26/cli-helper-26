import functools
import os
import threading

class ConfigRegistry:
    _storage = {}
    _lock = threading.Lock()

    def __init__(self):
        self._cache = {}

    @classmethod
    @functools.lru_cache(maxsize=128)
    def fetch_env(cls, key: str, default: str = None):
        with cls._lock:
            return os.environ.get(key, default)

    def get_optimized(self, key: str):
        if key not in self._cache:
            val = self.fetch_env(key)
            self._cache[key] = val
        return self._cache[key]

    def batch_load(self, keys: list):
        return {k: self.get_optimized(k) for k in keys}

    def __getitem__(self, item):
        return self.get_optimized(item)

    def __repr__(self):
        return f"<ConfigRegistry: {len(self._cache)} items cached>"

config_instance = ConfigRegistry()

def get_config(key, default=None):
    val = config_instance.get_optimized(key)
    return val if val is not None else default