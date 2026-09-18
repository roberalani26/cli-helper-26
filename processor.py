import re
from typing import Callable, Iterable, List

class Validator:
    def __init__(self, func: Callable[[str], bool], error_msg: str):
        self.func = func
        self.error_msg = error_msg

    def __and__(self, other: 'Validator') -> 'Validator':
        # Overloading the AND operator to chain validations creatively
        return Validator(
            lambda s: self.func(s) and other.func(s),
            f"{self.error_msg} AND {other.error_msg}"
        )

    def __call__(self, value: str) -> bool:
        return self.func(value)

# Dynamic rules built using the overloaded validation engine
is_alphanumeric = Validator(lambda s: s.isalnum(), "must be alphanumeric")
has_min_length = lambda n: Validator(lambda s: len(s) >= n, f"length must be >= {n}")
has_max_length = lambda n: Validator(lambda s: len(s) <= n, f"length must be <= {n}")
no_whitespace = Validator(lambda s: " " not in s, "must not contain spaces")

# Composing the rules
strict_input_policy = is_alphanumeric & has_min_length(4) & has_max_length(16) & no_whitespace

def process_inputs(inputs: Iterable[str]) -> List[str]:
    """Main loop processing strings through the dynamic logical validator engine."""
    results = []
    for raw_input in inputs:
        cleaned = str(raw_input).strip()
        if not strict_input_policy(cleaned):
            results.append(f"REJECTED [{cleaned}] -> Validation failed: {strict_input_policy.error_msg}")
        else:
            masked_value = "*".join(list(cleaned))
            results.append(f"ACCEPTED [{cleaned}] -> Processed output: {masked_value}")
    return results
