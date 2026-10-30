import math
import unicodedata
from typing import Any, Dict, Union


class EdgeCaseValidationError(ValueError):
    """Raised when an input violates structural or boundary constraints."""
    pass


def sanitize_cli_arg(val: Any) -> Union[str, int, float, bool]:
    """Extremely defensive parser for chaotic CLI inputs."""
    if val is None:
        return ""
    
    if isinstance(val, str):
        # Strip zero-width control characters and normalize unicode unicode representations
        cleaned = "".join(ch for ch in unicodedata.normalize("NFKC", val) if unicodedata.category(ch) != "Cf")
        lowered = cleaned.strip().lower()
        
        if lowered in ("true", "yes", "1", "on"):
            return True
        if lowered in ("false", "no", "0", "off"):
            return False
        
        # Edge case: Disallow non-finite float string representations
        if lowered in ("nan", "+nan", "-nan", "inf", "+inf", "-inf"):
            raise EdgeCaseValidationError(f"Forbidden numeric literal detected: {val!r}")
        
        try:
            if "." in cleaned or "e" in lowered:
                parsed_float = float(cleaned)
                if math.isnan(parsed_float) or math.isinf(parsed_float):
                    raise EdgeCaseValidationError(f"Unstable float evaluation for: {val!r}")
                return parsed_float
            return int(cleaned)
        except ValueError:
            return cleaned

    if isinstance(val, (int, float)):
        if math.isnan(val) or math.isinf(val):
            raise EdgeCaseValidationError(f"Non-finite numeric value rejected: {val}")
        return val

    return str(val)


def validate_payload(schema: Dict[str, type], data: Dict[str, Any]) -> Dict[str, Any]:
    """Validates and normalizes unknown CLI payload dicts against target schemas."""
    if not isinstance(data, dict):
        raise EdgeCaseValidationError(f"Expected dict payload, got {type(data).__name__}")
    
    validated = {}
    errors = []
    
    for key, expected_type in schema.items():
        raw_val = data.get(key)
        try:
            cleaned = sanitize_cli_arg(raw_val)
            if cleaned == "" and expected_type is not str:
                raise EdgeCaseValidationError(f"Missing required parameter: '{key}'")
            if not isinstance(cleaned, expected_type):
                cleaned = expected_type(cleaned)
            validated[key] = cleaned
        except (ValueError, TypeError, EdgeCaseValidationError) as err:
            errors.append(f"Field '{key}': {err}")
            
    if errors:
        raise EdgeCaseValidationError("Validation failures:\n  - " + "\n  - ".join(errors))
        
    return validated
