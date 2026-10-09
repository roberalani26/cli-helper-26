import re
from typing import Any, Callable, Dict, Optional

class ValidatorRegistry:
    def __init__(self):
        self._rules: Dict[str, Callable[[Any], bool]] = {
            "email": lambda x: bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", str(x))),
            "integer": lambda x: str(x).isdigit(),
            "slug": lambda x: bool(re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", str(x)))
        }

    def validate(self, field_type: str, value: Any) -> bool:
        return self._rules.get(field_type, lambda _: True)(value)

    def register(self, field_type: str, func: Callable[[Any], bool]) -> None:
        self._rules[field_type] = func

def run_pipeline(data: Dict[str, Any], schema: Dict[str, str]) -> Dict[str, bool]:
    registry = ValidatorRegistry()
    return {k: registry.validate(schema[k], v) for k, v in data.items() if k in schema}

if __name__ == "__main__":
    data_payload = {"user": "dev@example.com", "id": "123", "repo": "cli-helper-26"}
    schema_map = {"user": "email", "id": "integer", "repo": "slug"}
    print(run_pipeline(data_payload, schema_map))