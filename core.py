import functools
import sys
import time
from typing import Any, Callable, Dict, List, Tuple


class CachedDescriptor:
    """Slot-based fast descriptor for caching computed CLI command results."""

    __slots__ = ("_func", "_cache", "_maxsize")

    def __init__(self, maxsize: int = 256):
        self._func: Callable[..., Any] | None = None
        self._cache: Dict[Tuple[Any, ...], Any] = {}
        self._maxsize = maxsize

    def __call__(self, func: Callable[..., Any]) -> "CachedDescriptor":
        self._func = func
        return self

    def __get__(self, instance: Any, owner: Any) -> Callable[..., Any]:
        if instance is None:
            return self

        @functools.wraps(self._func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, tuple(sorted(kwargs.items())))
            if key in self._cache:
                return self._cache[key]

            result = self._func(instance, *args, **kwargs)
            if len(self._cache) >= self._maxsize:
                self._cache.pop(next(iter(self._cache)))
            self._cache[key] = result
            return result

        return wrapper


class CoreCommandPipeline:
    """High-performance execution engine for CLI operations."""

    __slots__ = ("_registry", "_metrics")

    def __init__(self) -> None:
        self._registry: Dict[str, Callable[..., Any]] = {}
        self._metrics: List[float] = []

    def register(self, name: str, fn: Callable[..., Any]) -> None:
        self._registry[name] = fn

    @CachedDescriptor(maxsize=128)
    def transform_output(self, template: str, data: Tuple[Tuple[str, str], ...]) -> str:
        """Optimized template renderer avoiding regex overhead."""
        result = template
        for key, value in data:
            result = result.replace(f"{{{key}}}", value)
        return result

    def execute_batch(self, tasks: List[Tuple[str, Dict[str, Any]]]) -> List[Any]:
        """Process batch of CLI calls with execution timing."""
        start_time = time.perf_counter()
        results = []
        for cmd_name, kwargs in tasks:
            if cmd_name in self._registry:
                results.append(self._registry[cmd_name](**kwargs))
        self._metrics.append(time.perf_counter() - start_time)
        return results
