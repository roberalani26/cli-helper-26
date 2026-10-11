import re
from typing import Callable, Tuple

class ValidationChain:
    def __init__(self, *rules: Callable[[str], bool | str]):
        self.rules = rules

    def __rshift__(self, other: Callable[[str], bool | str]) -> "ValidationChain":
        return ValidationChain(*self.rules, other)

    def validate(self, payload: str) -> Tuple[bool, str]:
        for rule in self.rules:
            res = rule(payload)
            if res is not True:
                reason = res if isinstance(res, str) else getattr(rule, "__name__", "anonymous_rule")
                return False, f"Rule failed: {reason}"
        return True, "Valid"

is_non_empty = lambda s: len(s.strip()) > 0 or "Input cannot be empty"
is_safe_chars = lambda s: bool(re.match(r"^[a-zA-Z0-9_\-\s\.]+$", s)) or "Contains forbidden characters"
within_length = lambda s: len(s) <= 64 or "Exceeds maximum length of 64"
no_reserved = lambda s: s.strip().lower() not in {"exit", "quit", "root"} or "Reserved keyword"

PIPELINE = ValidationChain() >> is_non_empty >> is_safe_chars >> within_length >> no_reserved

def run_loop(stream: list[str]) -> list[str]:
    results = []
    for line in stream:
        is_valid, err = PIPELINE.validate(line)
        if not is_valid:
            results.append(f"SKIP ({err}): {line!r}")
            continue
        cleaned = line.strip().lower()
        results.append(f"PROCESSED: {cleaned}")
    return results

if __name__ == "__main__":
    test_stream = ["", "valid_cmd", "bad;cmd", "root", "a" * 100]
    for out in run_loop(test_stream):
        print(out)