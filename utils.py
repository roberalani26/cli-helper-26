"""Data handling utility with fluent structural transformation and pipeline mechanics."""

from typing import Any, Callable, Generator


class DataPipeline:
    """Fluent data manipulation wrapper for complex nested structures."""

    def __init__(self, data: Any):
        self._data = data

    @property
    def raw(self) -> Any:
        return self._data

    def flatten(self, sep: str = ".") -> "DataPipeline":
        def _flatten_gen(obj: Any, parent_key: str = "") -> Generator[tuple[str, Any], None, None]:
            if isinstance(obj, dict):
                for k, v in obj.items():
                    new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
                    yield from _flatten_gen(v, new_key)
            elif isinstance(obj, (list, tuple)):
                for i, v in enumerate(obj):
                    new_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
                    yield from _flatten_gen(v, new_key)
            else:
                yield parent_key, obj

        if isinstance(self._data, (dict, list, tuple)):
            return DataPipeline(dict(_flatten_gen(self._data)))
        return self

    def unflatten(self, sep: str = ".") -> "DataPipeline":
        if not isinstance(self._data, dict):
            return self
        result: dict[str, Any] = {}
        for key, value in self._data.items():
            parts = str(key).split(sep)
            curr = result
            for part in parts[:-1]:
                if part not in curr or not isinstance(curr[part], dict):
                    curr[part] = {}
                curr = curr[part]
            curr[parts[-1]] = value
        return DataPipeline(result)

    def map_values(self, fn: Callable[[Any], Any]) -> "DataPipeline":
        def _rec_map(obj: Any) -> Any:
            if isinstance(obj, dict):
                return {k: _rec_map(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [_rec_map(v) for v in obj]
            return fn(obj)

        return DataPipeline(_rec_map(self._data))

    def __getitem__(self, path: str) -> Any:
        curr = self._data
        for key in path.split("."):
            if isinstance(curr, dict) and key in curr:
                curr = curr[key]
            elif isinstance(curr, (list, tuple)) and key.isdigit() and int(key) < len(curr):
                curr = curr[int(key)]
            else:
                raise KeyError(f"Path part '{key}' not found in structure")
        return curr


def shape(data: Any) -> DataPipeline:
    """Wrap arbitrary data in a fluent DataPipeline transformer."""
    return DataPipeline(data)
