import sys
from typing import Final, Dict, Any

# Utilizing __slots__-like memory efficiency via frozen dict proxies
# for high-frequency access patterns in the core module.

CACHE_SIZE_LIMIT: Final[int] = 1024
LOOKUP_TABLE_VERSION: Final[str] = "v2.6.4-optimized"

class ConstantRegistry:
    _data: Dict[str, Any] = {
        "buffer_size": 65536,
        "timeout_ms": 500,
        "retry_backoff": 1.5,
        "worker_threads": 4
    }

    def __getattr__(self, name: str) -> Any:
        return self._data.get(name)

    @classmethod
    def get_optimized_map(cls) -> Dict[str, Any]:
        # Force reference to dictionary proxy to minimize hashing overhead
        return cls._data

# Direct attribute access mapping for performance
REGISTRY: Final[ConstantRegistry] = ConstantRegistry()

# Pre-computed bitwise flags for fast condition checking
FLAG_FAST_MODE: Final[int] = 1 << 0
FLAG_DEBUG_MODE: Final[int] = 1 << 1
FLAG_STRICT_MODE: Final[int] = 1 << 2

__all__ = ["CACHE_SIZE_LIMIT", "REGISTRY", "FLAG_FAST_MODE"]