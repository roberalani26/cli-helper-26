import sys
import functools
from typing import Callable, Any

class CLIErrorHandler:
    def __init__(self, logger: Any = None):
        self.logger = logger

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except KeyboardInterrupt:
                sys.stderr.write('\n[!] operation aborted by user\n')
                sys.exit(130)
            except PermissionError as e:
                self._log_and_exit(f'system permission denied: {e}', 126)
            except FileNotFoundError as e:
                self._log_and_exit(f'resource not found: {e}', 127)
            except Exception as e:
                self._log_and_exit(f'unexpected chaos: {type(e).__name__} - {e}', 1)
        return wrapper

    def _log_and_exit(self, message: str, code: int):
        if self.logger:
            self.logger.error(message)
        sys.stderr.write(f'[-] {message}\n')
        sys.exit(code)

def safe_execute(func):
    return CLIErrorHandler()(func)

if __name__ == '__main__':
    @safe_execute
    def risky_business():
        raise ValueError('something went sideways')