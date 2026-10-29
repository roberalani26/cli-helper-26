import sys
from typing import Callable, Generator, Tuple


class Rule:
    """Composable input validator using operator overloading for CLI streams."""

    def __init__(self, predicate: Callable[[str], bool], message: str):
        self.predicate = predicate
        self.message = message

    def validate(self, value: str) -> Tuple[bool, str]:
        try:
            ok = bool(self.predicate(value))
            return ok, "" if ok else self.message
        except Exception as err:
            return False, f"Evaluation failed: {err}"

    def __and__(self, other: "Rule") -> "Rule":
        def composed(val: str) -> bool:
            return self.validate(val)[0] and other.validate(val)[0]

        return Rule(composed, f"{self.message}; {other.message}")

    def __or__(self, other: "Rule") -> "Rule":
        def composed(val: str) -> bool:
            return self.validate(val)[0] or other.validate(val)[0]

        return Rule(composed, f"({self.message} OR {other.message})")


def validate_loop_stream(
    inputs: Generator[str, None, None],
    rule: Rule
) -> Generator[Tuple[str, bool, str], None, None]:
    """Yield validated tokens from the main processing loop stream."""
    for raw in inputs:
        token = raw.strip()
        if not token:
            continue
        is_valid, err_msg = rule.validate(token)
        yield token, is_valid, err_msg


# Standard validation rules for cli-helper-26
NON_EMPTY = Rule(lambda s: len(s) > 0, "input cannot be empty")
SAFE_CHARS = Rule(lambda s: all(c.isalnum() or c in "_.- " for c in s), "contains unsafe characters")
MAX_LEN = Rule(lambda s: len(s) <= 128, "input exceeds maximum length of 128")

MAIN_LOOP_RULE = NON_EMPTY & SAFE_CHARS & MAX_LEN
