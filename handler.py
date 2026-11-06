import sys
import logging
from functools import wraps

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger('cli-helper-26')

class EdgeCaseRegistry:
    def __init__(self):
        self.hooks = {}

    def register(self, exception_type):
        def decorator(func):
            self.hooks[exception_type] = func
            return func
        return decorator

registry = EdgeCaseRegistry()

@registry.register(ValueError)
def handle_value_error(e):
    return f"Critical conversion failure: {e}"

@registry.register(TypeError)
def handle_type_error(e):
    return f"Type mismatch detected: {e}"

def resilient_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            handler = registry.hooks.get(type(e))
            if handler:
                return handler(e)
            logger.error(f"Unhandled fallout: {str(e)}")
            return None
    return wrapper

def process_input(data):
    if not isinstance(data, int):
        raise TypeError("Expected integer input")
    if data < 0:
        raise ValueError("Negative values forbidden")
    return data * 42