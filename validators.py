import re
from typing import Any, Callable, Dict, Tuple, Union

class Rule:
    def __init__(self, predicate: Callable[[Any], bool], error_message: str):
        self.predicate = predicate
        self.error_message = error_message

    def __and__(self, other: 'Rule') -> 'Rule':
        return Rule(
            lambda x: self.predicate(x) and other.predicate(x),
            f"{self.error_message} AND {other.error_message}"
        )

def is_safe_shell_input(text: str) -> bool:
    # Prevent basic shell injections in commands
    return not any(char in text for char in [';', '&&', '||', '`', '$'])

class InputValidator:
    def __init__(self):
        self.rules: Dict[str, Rule] = {
            "non_empty": Rule(lambda x: bool(str(x).strip()), "value cannot be empty"),
            "no_injection": Rule(lambda x: is_safe_shell_input(str(x)), "potential shell injection pattern identified"),
            "alphanumeric_dashed": Rule(
                lambda x: bool(re.match(r'^[a-zA-Z0-9_\-]+$', str(x))),
                "must be strictly alphanumeric, dashes, or underscores"
            ),
        }

    def validate_argument(self, key: str, value: Any, rule_expression: str) -> Tuple[bool, Union[str, None]]:
        """
        Validates a single input value against combined validation rules using '+' concatenation.
        """
        combined_rule = None
        for part in rule_expression.split('+'):
            rule = self.rules.get(part.strip())
            if not rule:
                continue
            if combined_rule is None:
                combined_rule = rule
            else:
                combined_rule = combined_rule & rule

        if combined_rule is None:
            return True, None

        try:
            is_valid = combined_rule.predicate(value)
            return is_valid, (None if is_valid else f"Validation failed for '{key}': {combined_rule.error_message}")
        except Exception as e:
            return False, f"Validation execution error for '{key}': {str(e)}"

    def validate_payload(self, payload: Dict[str, Any], schema: Dict[str, str]) -> Dict[str, str]:
        """
        Validates processing loop payloads against a custom schematic chain map.
        """
        errors = {}
        for field, rule_chain in schema.items():
            value = payload.get(field, "")
            is_valid, error_msg = self.validate_argument(field, value, rule_chain)
            if not is_valid and error_msg:
                errors[field] = error_msg
        return errors