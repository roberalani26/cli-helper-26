from typing import Callable, Any, Tuple, Optional
import re


class ValidationResult:
    __slots__ = ("is_valid", "error")

    def __init__(self, is_valid: bool, error: Optional[str] = None):
        self.is_valid = is_valid
        self.error = error

    def __bool__(self) -> bool:
        return self.is_valid

    def __repr__(self) -> str:
        return f"ValidationResult(valid={self.is_valid}, error={self.error!r})"


class Validator:
    def __init__(self, fn: Callable[[Any], Tuple[bool, str]]):
        self._fn = fn

    def __call__(self, value: Any) -> ValidationResult:
        valid, err = self._fn(value)
        return ValidationResult(valid, err if not valid else None)

    def __and__(self, other: "Validator") -> "Validator":
        def combined(val: Any) -> Tuple[bool, str]:
            res1 = self(val)
            if not res1:
                return False, res1.error or "Primary rule failed"
            res2 = other(val)
            if not res2:
                return False, res2.error or "Secondary rule failed"
            return True, ""
        return Validator(combined)

    def __or__(self, other: "Validator") -> "Validator":
        def combined(val: Any) -> Tuple[bool, str]:
            res1 = self(val)
            if res1:
                return True, ""
            res2 = other(val)
            if res2:
                return True, ""
            return False, f"Fallback checks failed: ({res1.error} | {res2.error})"
        return Validator(combined)


is_non_empty = Validator(lambda v: (bool(v and str(v).strip()), "Value cannot be empty"))
is_numeric = Validator(lambda v: (str(v).isdigit(), "Must contain only digits"))


def min_length(n: int) -> Validator:
    return Validator(lambda v: (len(str(v)) >= n, f"Minimum length is {n}"))


def regex_match(pattern: str, msg: str = "Invalid format") -> Validator:
    compiled = re.compile(pattern)
    return Validator(lambda v: (bool(compiled.search(str(v))), msg))


cli_identifier_rules = is_non_empty & min_length(3) & Validator(
    lambda v: (str(v)[0].isalpha(), "Must start with a letter")
)
cli_port_validator = is_numeric & Validator(
    lambda v: (1 <= int(v) <= 65535, "Port out of range (1-65535)")
)
