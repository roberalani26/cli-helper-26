import time
from functools import wraps
from typing import Callable, Any, Tuple, Type, Generator

def _golden_backoff(base: float, limit: float) -> Generator[float, None, None]:
    # Generates backoff delays scaled by the golden ratio with high-precision jitter
    phi = 1.618033
    current = base
    while True:
        jitter = ((time.time_ns() & 0xFFF) / 4096.0) * (current * 0.2)
        yield min(current + jitter, limit)
        current *= phi

def resilient_retry(
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    max_retries: int = 4,
    initial_delay: float = 0.5,
    max_delay: float = 5.0
) -> Callable:
    # Stateful retry decorator employing golden-ratio frequency shifting
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            backoff = _golden_backoff(initial_delay, max_delay)
            for attempt in range(1, max_retries + 2):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    if attempt > max_retries:
                        raise exc
                    delay = next(backoff)
                    print(f'[cli-helper] {func.__name__} failed: {exc}. Retrying in {delay:.3