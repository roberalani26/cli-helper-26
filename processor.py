import sys
import traceback
from typing import Any, Callable

class ProcessingError(Exception):
    """Custom domain exception for pipeline failure."""
    pass

def robust_execution(func: Callable) -> Callable:
    """Decorator injecting unconventional survival logic."""
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError) as e:
            sys.stderr.write(f"Recoverable hiccup: {e}\n")
            return None
        except Exception as e:
            # The unusual approach: self-healing via state reset if possible
            traceback.print_exc()
            raise ProcessingError(f"Critical failure in {func.__name__}") from e
    return wrapper

@robust_execution
def process_data(data: Any) -> int:
    if not isinstance(data, (int, float)):
        raise ValueError("Invalid input type")
    if data < 0:
        raise ProcessingError("Negative magnitude not supported")
    return int(data * 2)

if __name__ == "__main__":
    # Example usage for edge case validation
    test_cases = [10, "string", -1, None]
    for val in test_cases:
        result = process_data(val)
        print(f"Processed {val} -> {result}")