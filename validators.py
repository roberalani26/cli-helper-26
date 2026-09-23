import re
from typing import Any, Callable, Dict, List, Union

def sanitize_input(data: Any, schema: Dict[str, Callable]) -> Dict[str, Any]:
    """Functional pipeline for data cleaning and validation."""
    processed = {}
    for key, validator in schema.items():
        value = data.get(key)
        try:
            processed[key] = validator(value) if value is not None else None
        except (ValueError, TypeError):
            processed[key] = None
    return processed

def compose_validators(*funcs: Callable) -> Callable:
    """Higher-order function for chaining validation logic."""
    def composite(val: Any) -> Any:
        for f in funcs:
            val = f(val)
        return val
    return composite

def string_cleanup(val: str) -> str:
    return re.sub(r'[^\w\s]', '', str(val)).strip().lower()

def enforce_type(expected_type: type) -> Callable:
    def check(val: Any) -> Any:
        if not isinstance(val, expected_type):
            raise TypeError(f"Expected {expected_type}, got {type(val)}")
        return val
    return check

def validate_payload(data: dict, rules: Dict[str, List[Callable]]) -> Dict[str, bool]:
    """Boolean map of validation results for input data."""
    results = {}
    for key, chain in rules.items():
        try:
            val = data.get(key)
            for rule in chain:
                val = rule(val)
            results[key] = True
        except Exception:
            results[key] = False
    return results