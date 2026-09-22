import sys
import traceback
from typing import Callable, Any, Dict, List

class FaultTolerantHandler:
    """Wraps CLI execution with unconventional recovery strategies for weird edge cases."""
    
    def __init__(self, fallback_default: Any = None):
        self.fallback_default = fallback_default
        self._strategies: List[Callable[[Exception, tuple, dict], Any]] = []
        self._register_default_strategies()

    def register_strategy(self, strategy: Callable[[Exception, tuple, dict], Any]):
        self._strategies.append(strategy)
        return strategy

    def _register_default_strategies(self):
        @self.register_strategy
        def handle_type_error(exc, args, kwargs):
            if isinstance(exc, TypeError):
                new_args = tuple(str(a) if a is not None else "" for a in args)
                return ("healed", new_args, kwargs)
            return None

        @self.register_strategy
        def handle_encoding_error(exc, args, kwargs):
            if isinstance(exc, (UnicodeEncodeError, UnicodeDecodeError)):
                safe_args = tuple(
                    a.encode('utf-8', errors='ignore').decode('utf-8') if isinstance(a, str) else a 
                    for a in args
                )
                return ("healed", safe_args, kwargs)
            return None

    def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Executes a function, trying healing strategies sequentially on failure."""
        try:
            return func(*args, **kwargs)
        except Exception as primary_exception:
            for strategy in self._strategies:
                try:
                    remedy = strategy(primary_exception, args, kwargs)
                    if remedy and remedy[0] == "healed":
                        _, new_args, new_kwargs = remedy
                        return func(*new_args, **new_kwargs)
                except Exception:
                    continue
            
            sys.stderr.write(f"[CLI-HELPER-ERR] Unrecoverable anomaly: {primary_exception}\n")
            sys.stderr.write(f"[CLI-HELPER-ERR] Traceback summary: {traceback.format_exc(limit=1)}\n")
            return self.fallback_default

def safe_run(func: Callable, *args, **kwargs) -> Any:
    handler = FaultTolerantHandler(fallback_default="ERR_HALT")
    return handler.execute(func, *args, **kwargs)