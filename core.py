import functools
from typing import Callable, Any, Dict, Tuple


class FastCommandRegistry:
    """High-performance command dispatcher utilizing slot memoization and packed trie routing."""

    __slots__ = ('_trie', '_cache', '_max_cache_size')

    def __init__(self, max_cache_size: int = 1024):
        self._trie: Dict[str, Any] = {}
        self._cache: Dict[Tuple[str, ...], Callable[..., Any]] = {}
        self._max_cache_size = max_cache_size

    def register(self, path: str) -> Callable:
        """Decorator registering command handlers into a prefix trie."""
        tokens = tuple(path.strip().split())

        def decorator(func: Callable) -> Callable:
            node = self._trie
            for token in tokens:
                node = node.setdefault(token, {})
            node['__exec__'] = func
            self._cache.clear()
            return func

        return decorator

    def __call__(self, raw_cmd: str, *args, **kwargs) -> Any:
        """Fast-path resolution using tuple keys and inline trie traversal."""
        tokens = tuple(raw_cmd.strip().split())

        handler = self._cache.get(tokens)
        if handler:
            return handler(*args, **kwargs)

        node = self._trie
        for token in tokens:
            if token not in node:
                raise KeyError(f"Command path not found: {raw_cmd}")
            node = node[token]

        if '__exec__' not in node:
            raise ValueError(f"Incomplete command path: {raw_cmd}")

        handler = node['__exec__']
        if len(self._cache) < self._max_cache_size:
            self._cache[tokens] = handler

        return handler(*args, **kwargs)


dispatcher = FastCommandRegistry()


@dispatcher.register("sys status")
def _sys_status(verbose: bool = False) -> str:
    return f"OK (verbose={verbose})"


@dispatcher.register("sys config reload")
def _config_reload() -> bool:
    return True


def run_command(raw_input: str, *args, **kwargs) -> Any:
    return dispatcher(raw_input, *args, **kwargs)
