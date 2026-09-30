import functools
from typing import Any, Callable, List, Union


class StreamPipe:
    """A lightweight, operator-overloaded data processor for CLI streams."""

    def __init__(self, data: Any = None):
        self._data = data
        self._ops: List[Callable[[Any], Any]] = []

    def __rshift__(self, other: Union[Callable[[Any], Any], "StreamPipe"]) -> "StreamPipe":
        new_pipe = StreamPipe(self._data)
        new_pipe._ops = list(self._ops)
        if callable(other):
            new_pipe._ops.append(other)
        elif isinstance(other, StreamPipe):
            new_pipe._ops.extend(other._ops)
        return new_pipe

    def __call__(self, initial_data: Any = None) -> Any:
        target = initial_data if initial_data is not None else self._data
        return functools.reduce(lambda val, op: op(val), self._ops, target)

    def collect(self) -> Any:
        return self.__call__()


def flatten_nested(data: Any, sep: str = ".") -> dict:
    """Flattens a deeply nested dictionary or list structure."""

    def _flatten(obj, prefix=""):
        items = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_key = f"{prefix}{sep}{k}" if prefix else str(k)
                items.extend(_flatten(v, new_key).items())
        elif isinstance(obj, (list, tuple)):
            for i, v in enumerate(obj):
                new_key = f"{prefix}[{i}]"
                items.extend(_flatten(v, new_key).items())
        else:
            items.append((prefix, obj))
        return dict(items)

    return _flatten(data)


def filter_keys(predicate: Callable[[str], bool]) -> Callable[[dict], dict]:
    """Returns a transformer function that filters dict keys by a predicate."""
    return lambda d: {
        k: v for k, v in d.items() if predicate(str(k))
    } if isinstance(d, dict) else d
