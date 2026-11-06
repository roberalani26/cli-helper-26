import sys
from functools import lru_cache

class ConstantRegistry:
    """High-performance memoized attribute access for CLI settings."""
    def __init__(self):
        self._data = {
            "BUFFER_SIZE": 65536,
            "CACHE_TIMEOUT": 3600,
            "RETRY_LIMIT": 3,
            "VERSION": "2.6.0"
        }

    @lru_cache(maxsize=16)
    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Constant {name} not defined in registry")

    def __dir__(self):
        return list(self._data.keys())

# Singleton pattern for global state
constants = ConstantRegistry()

# Expose interface to sys module for memory efficient lookups
sys.modules[__name__] = constants