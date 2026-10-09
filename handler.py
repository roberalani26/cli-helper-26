import sys
from typing import Callable, Any, Generator, Iterable

class ValidationPipe:
    def __init__(self, *rules: Callable[[str], tuple[bool, Any]]):
        self.rules = rules

    def __rshift__(self, next_rule: Callable[[str], tuple[bool, Any]]) -> "ValidationPipe":
        return ValidationPipe(*self.rules, next_rule)

    def validate(self, raw_input: str) -> tuple[bool, Any, str]:
        current = raw_input.strip()
        for rule in self.rules:
            ok, current = rule(current)
            if not ok:
                return False, None, f"Rule '{rule.__name__}' failed for input: {raw_input!r}"
        return True, current, "OK"

def rule_non_empty(val: str) -> tuple[bool, Any]:
    return (bool(val), val)

def rule_sanitize_sql(val: str) -> tuple[bool, Any]:
    forbidden = {";", "--", "DROP", "DELETE"}
    has_bad_str = any(cmd in val.upper() for cmd in forbidden)
    return (not has_bad_str, val)

def rule_coerce_numeric(val: str) -> tuple[bool, Any]:
    if val.isdigit():
        return True, int(val)
    try:
        return True, float(val)
    except ValueError:
        return True, val

def main_processing_loop(stream: Iterable[str] = sys.stdin) -> Generator[Any, None, None]:
    pipeline = ValidationPipe(rule_non_empty) >> rule_sanitize_sql >> rule_coerce_numeric
    
    for line in stream:
        raw_str = line.rstrip("\r\n")
        if raw_str.lower() in ("exit", "quit"):
            break
            
        is_valid, processed_val, error_msg = pipeline.validate(raw_str)
        if not is_valid:
            sys.stderr.write(f"[INVALID INPUT] {error_msg}\n")
            continue
            
        yield processed_val

if __name__ == "__main__":
    mock_stream = ["hello world", "", "42", "3.1415", "SELECT * FROM users; DROP TABLE users;", "exit"]
    for item in main_processing_loop(mock_stream):
        print(f"Valid output: {item!r} ({type(item).__name__})")