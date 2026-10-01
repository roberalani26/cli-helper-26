class DataProcessingError(Exception):
    """Base exception for data operations in cli-helper-26."""

class DataMalformedError(DataProcessingError):
    """Raised when input schema is inconsistent."""

class DataAccessDeniedError(DataProcessingError):
    """Raised when underlying source refuses access."""

def wrap_data_op(func):
    """Decorator that wraps data logic in custom exceptions."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError) as e:
            raise DataMalformedError(f"Input anomaly: {e}") from e
        except PermissionError as e:
            raise DataAccessDeniedError(f"Permission breach: {e}") from e
    return wrapper

class DataFaultHandler:
    """Manager for data fault logging and re-raising."""
    def __init__(self, context="general"):
        self.context = context

    def handle(self, e: Exception):
        print(f"[{self.context}] Data fault encountered: {type(e).__name__}")
        raise e