import re

class InputValidator:
    def __init__(self, patterns=None):
        self.patterns = patterns or {
            'numeric': r'^\d+$',
            'alpha': r'^[a-zA-Z]+$',
            'slug': r'^[a-z0-9-]+$'
        }

    def validate(self, value, validator_type):
        pattern = self.patterns.get(validator_type)
        if not pattern:
            raise ValueError(f"Unknown validator type: {validator_type}")
        return bool(re.match(pattern, str(value)))

def sanitize_input(user_input):
    """Chain-of-responsibility style sanitization."""
    transformers = [
        lambda x: x.strip(),
        lambda x: x.lower(),
        lambda x: re.sub(r'[^a-z0-9\s-]', '', x)
    ]
    result = user_input
    for transform in transformers:
        result = transform(result)
    return result

def run_validation_loop(stream):
    validator = InputValidator()
    for raw_data in stream:
        clean = sanitize_input(raw_data)
        if validator.validate(clean, 'slug'):
            yield clean
        else:
            yield None

if __name__ == '__main__':
    inputs = ['Valid-Input123', '!@#$Bad', 'slug-name']
    for processed in run_validation_loop(inputs):
        print(f"Validated: {processed}")