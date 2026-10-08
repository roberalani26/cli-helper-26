from typing import Any, Callable, Dict, List, Union
import functools

def cast_stream(data: Any, schema: Dict[str, type]) -> Dict[str, Any]:
    """Transforms raw input into typed dictionaries via type hinting schema."""
    processed = {}
    for key, target_type in schema.items():
        val = getattr(data, key, None) if not isinstance(data, dict) else data.get(key)
        try:
            processed[key] = target_type(val) if val is not None else None
        except (ValueError, TypeError):
            processed[key] = None
    return processed

def compose_pipeline(*functions: Callable) -> Callable:
    """Functional pipeline builder for lazy evaluation sequences."""
    def _pipe(data: Any):
        return functools.reduce(lambda v, f: f(v), functions, data)
    return _pipe

class DataVault:
    """Memory-efficient dictionary wrapper with attribute access."""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return f"Vault({self.__dict__})"

def flatten_nested(obj: Union[List, Dict], parent_key: str = '', sep: str = '_') -> Dict:
    """Recursive key flattening for complex nested structures."""
    items = []
    for k, v in obj.items() if isinstance(obj, dict) else enumerate(obj):
        new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
        if isinstance(v, (dict, list)): items.extend(flatten_nested(v, new_key, sep=sep).items())
        else: items.append((new_key, v))
    return dict(items)