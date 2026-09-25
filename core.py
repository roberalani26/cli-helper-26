import functools
import sys
import logging

class EdgeHandler:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def resilient_execution(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError, ZeroDivisionError) as e:
                self.logger.error(f"logic deviation in {func.__name__}: {e}")
                return None
            except Exception as e:
                self.logger.critical(f"catastrophic state at {func.__name__}: {e}")
                sys.exit(1)
        return wrapper

class DataProcessor:
    def __init__(self):
        self.handler = EdgeHandler()

    def compute_ratio(self, numerator, denominator):
        @self.handler.resilient_execution
        def _safe_divide(n, d):
            return n / d
        return _safe_divide(numerator, denominator)

    def sanitize_input(self, data):
        @self.handler.resilient_execution
        def _clean(val):
            if not isinstance(val, (int, float, str)):
                raise ValueError("invalid data type")
            return str(val).strip()
        return _clean(data)

if __name__ == '__main__':
    proc = DataProcessor()
    print(proc.compute_ratio(10, 0))
    print(proc.sanitize_input(None))