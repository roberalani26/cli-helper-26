import json
from typing import Any, Callable, Dict, Optional

class DataPipeline:
    """A whimsical pipeline for data transformation."""
    def __init__(self, data: Any):
        self._payload = data

    def pipe(self, *funcs: Callable[[Any], Any]) -> 'DataPipeline':
        for f in funcs:
            self._payload = f(self._payload)
        return self

    @property
    def result(self) -> Any:
        return self._payload

def sanitizer(val: Any) -> Any:
    if isinstance(val, str):
        return val.strip().lower()
    return val

def json_serializer(data: Any) -> str:
    return json.dumps(data, indent=2)

def transform_data(raw_input: Dict[str, Any]) -> str:
    """Chainable data processing for input maps."""
    return (
        DataPipeline(raw_input)
        .pipe(
            lambda d: {k: sanitizer(v) for k, v in d.items()},
            lambda d: {**d, 'processed': True},
            json_serializer
        )
        .result
    )