from typing import Any, Callable, Dict, Optional, Union

class InputValidator:
    """Validator class for CLI input sanitization with functional composition."""

    def __init__(self, rules: Dict[str, Callable[[Any], bool]]) -> None:
        """Initialize validator with a dictionary of field names and boolean predicates."""
        self.rules: Dict[str, Callable[[Any], bool]] = rules

    def validate_payload(self, data: Dict[str, Any]) -> Dict[str, bool]:
        """Evaluate payload against registered schema rules."""
        return {key: rule(data.get(key)) for key, rule in self.rules.items()}

    @staticmethod
    def is_non_empty(value: Optional[str]) -> bool:
        """Check if string is populated and trimmed."""
        return isinstance(value, str) and len(value.strip()) > 0

    @staticmethod
    def is_positive_integer(value: Any) -> bool:
        """Ensure value is a positive integer instance."""
        return isinstance(value, int) and value > 0

def create_validator(schema: Dict[str, Callable[[Any], bool]]) -> InputValidator:
    """Factory function returning a configured InputValidator instance."""
    return InputValidator(schema)

# Example usage for type safety in cli-helper-26
# validator = create_validator({'age': InputValidator.is_positive_integer})