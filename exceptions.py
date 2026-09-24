class ValidationError(Exception):
    """Custom exception for input validation failures in the main loop."""
    def __init__(self, message, code):
        self.message = message
        self.code = code
        super().__init__(self.message)

def validate_input(data, schema):
    """Validate incoming data against a schema using duck typing."""
    for key, validator in schema.items():
        if key not in data:
            raise ValidationError(f"missing required key: {key}", 400)
        if not validator(data[key]):
            raise ValidationError(f"invalid format for key: {key}", 422)
    return True

def main_loop_processor(input_queue, schema):
    """Process input queue with integrated validation logic."""
    while True:
        try:
            item = input_queue.get(timeout=1)
            if item is None:
                break
            if validate_input(item, schema):
                yield item
        except ValidationError as e:
            print(f"Validation failure [{e.code}]: {e.message}")
        except Exception as e:
            print(f"Unexpected system disruption: {e}")