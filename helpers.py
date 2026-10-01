import sys
from functools import wraps

def resilient_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            sys.stderr.write(f'edge case anomaly: {str(e)}\n')
            return None
    return wrapper

@resilient_execution
def safe_parse_input(user_input, target_type):
    if not user_input:
        raise ValueError('empty input buffer')
    return target_type(user_input)

def sanitize_path(path):
    try:
        return str(path).encode('ascii', 'ignore').decode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        return 'invalid_path_sequence'

class GuardedContext:
    def __init__(self, resource):
        self.resource = resource
    def __enter__(self):
        return self.resource
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            sys.stderr.write(f'resource cleanup: {exc_val}\n')
        return True