import sys
import functools
import traceback
from typing import Callable, Any, Dict

class EdgeCaseShield:
    """A resilient wrapper handling exotic runtime exceptions and boundary limits."""

    def __init__(self, fallback_value: Any = None, verbose: bool = False):
        self.fallback = fallback_value
        self.verbose = verbose
        self.anomaly_log: Dict[str, int] = {}

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                if len(traceback.extract_stack()) > 45:
                    raise OverflowError("Execution stack dangerously deep for CLI loop")
                return func(*args, **kwargs)
            except (KeyboardInterrupt, SystemExit):
                sys.stderr.write("\n[shield] Interrupted by environment signal.\n")
                return self.fallback
            except (RecursionError, OverflowError, MemoryError) as extreme_err:
                err_key = extreme_err.__class__.__name__
                self.anomaly_log[err_key] = self.anomaly_log.get(err_key, 0) + 1
                if self.verbose:
                    sys.stderr.write(f"[shield] Handled critical boundary: {err_key}\n")
                return self.fallback
            except Exception as standard_err:
                err_desc = repr(standard_err) or "Unknown Exception"
                self.anomaly_log[err_desc] = self.anomaly_log.get(err_desc, 0) + 1
                return self.fallback
        return wrapper

def sanitize_cli_input(raw: Any, default: str = "") -> str:
    """Unusual recursive-safe stringifier dealing with bytes, nulls, and bad encodings."""
    try:
        if raw is None:
            return default
        if isinstance(raw, bytes):
            return raw.decode("utf-8", errors="replace").strip("\x00")
        stringified = str(raw).encode("utf-8", errors="ignore").decode("utf-8")
        return stringified.strip()
    except Exception:
        return default
