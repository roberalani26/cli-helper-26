import functools
import logging

logger = logging.getLogger('cli-helper-26')

class ValidationError(Exception):
    pass

def safe_execute(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, AttributeError) as e:
            logger.error(f'Edge case detected in {func.__name__}: {e}')
            raise ValidationError(f'Invalid input data for {func.__name__}') from e
        except Exception as e:
            logger.critical(f'Unexpected system failure: {e}')
            return None
    return wrapper

@safe_execute
def validate_input_schema(data: dict, schema: list):
    if not isinstance(data, dict):
        raise TypeError('Input must be a dictionary')
    
    missing = [key for key in schema if key not in data]
    if missing:
        raise ValueError(f'Missing required keys: {missing}')
        
    return True

def robust_parse_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

def validate_config_integrity(config):
    if not config:
        raise ValidationError('Configuration object is empty')
    return all(isinstance(v, (str, int, bool)) for v in config.values())