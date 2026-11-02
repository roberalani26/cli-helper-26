import sys
import re
import unicodedata
from typing import Any, Callable, Optional, Tuple, Union

class ValidationError(Exception):
    """Base exception raised when validation and recovery fail."""
    pass

class ValidationRule:
    """Validation rule wrapper with pipeline chaining via bitwise OR (|)."""

    def __init__(self, check_fn: Callable[[Any], Any], recovery_fn: Optional[Callable[[Any, Exception], Any]] = None):
        self.check_fn = check_fn
        self.recovery_fn = recovery_fn

    def __call__(self, value: Any) -> Any:
        try:
            return self.check_fn(value)
        except Exception as err:
            if self.recovery_fn:
                try:
                    return self.recovery_fn(value, err)
                except Exception as recovery_err:
                    raise ValidationError(f"Recovery failed for input {value!r}: {recovery_err}") from err
            raise ValidationError(f"Validation failed for input {value!r}: {err}") from err

    def __or__(self, next_rule: "ValidationRule") -> "ValidationRule":
        def combined(val: Any) -> Any:
            return next_rule(self(val))
        return ValidationRule(combined)

def sanitize_cli_arg(arg: Any) -> str:
    """Normalize unicode and strip dangerous invisible control characters."""
    if not isinstance(arg, (str, bytes)):
        arg = str(arg)
    if isinstance(arg, bytes):
        arg = arg.decode("utf-8", errors="replace")
    
    cleaned = unicodedata.normalize("NFKC", arg)
    cleaned = "".join(ch for ch in cleaned if unicodedata.category(ch)[0] != "C" or ch in "\n\t\r")
    if not cleaned.strip():
        raise ValueError("Input string is empty or contains only non-printable chars")
    return cleaned.strip()

def recover_malformed_flag(val: Any, err: Exception) -> str:
    """Attempt auto-repair of malformed flag arguments like --foo= or unclosed quotes."""
    raw = str(val).rstrip("=")
    if (raw.startswith('"') and not raw.endswith('"')) or (raw.startswith("'") and not raw.endswith("'")):
        raw = raw + raw[0]
    return sanitize_cli_arg(raw)

def parse_numeric_option(val: str) -> Union[int, float]:
    """Parse numeric input while guarding against infinity and NaN edge cases."""
    clean = str(val).strip().lower()
    if clean in ("inf", "-inf", "nan", "+inf"):
        raise ValueError("Infinite or NaN values are forbidden in CLI options")
    return float(clean) if "." in clean else int(clean)

def validate_cli_input(raw_input: Any) -> Tuple[str, Optional[Union[int, float]]]:
    """Execute pipeline with resilience against malformed tokens and edge cases."""
    str_rule = ValidationRule(sanitize_cli_arg, recovery_fn=recover_malformed_flag)
    num_rule = ValidationRule(parse_numeric_option, recovery_fn=lambda v, e: 0)
    
    clean_str = str_rule(raw_input)
    num_val = None
    if re.search(r"\d", clean_str):
        try:
            extracted = re.sub(r"[^\d.-]", "", clean_str)
            num_val = num_rule(extracted)
        except ValidationError:
            num_val = 0
            
    return clean_str, num_val
