import sys
from functools import lru_cache
from typing import Callable, Any, Dict, Tuple, Optional


class CoreEngine:
    """Optimized execution core using string interning and token-trie dispatching."""
    __slots__ = ('_tree', '_exec_count')

    def __init__(self) -> None:
        self._tree: Dict[str, Any] = {}
        self._exec_count: int = 0

    def register(self, route: str) -> Callable:
        """Registers a handler for a fast-path CLI route."""
        def wrapper(func: Callable) -> Callable:
            tokens = tuple(sys.intern(part) for part in route.strip().split())
            node = self._tree
            for token in tokens:
                node = node.setdefault(token, {})
            node['$'] = func
            self._resolve.cache_clear()
            return func
        return wrapper

    @lru_cache(maxsize=2048)
    def _resolve(self, tokens: Tuple[str, ...]) -> Tuple[Callable, Tuple[str, ...]]:
        node = self._tree
        idx = 0
        last_func: Optional[Callable] = None
        last_idx = 0

        for token in tokens:
            token_interned = sys.intern(token)
            if token_interned in node:
                node = node[token_interned]
                idx += 1
                if '$' in node:
                    last_func = node['$']
                    last_idx = idx
            else:
                break

        if last_func is not None:
            return last_func, tokens[last_idx:]
        raise ValueError(f"Unknown command sequence: {' '.join(tokens)}")

    def run(self, raw_input: str) -> Any:
        """Parse and execute a raw command string at high throughput."""
        tokens = tuple(raw_input.strip().split())
        if not tokens:
            return None
        self._exec_count += 1
        handler, leftover = self._resolve(tokens)
        return handler(*leftover)


engine = CoreEngine()
