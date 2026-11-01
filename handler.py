import sys
from typing import Any, Callable, Dict

class ExecutionContext:
    def __init__(self):
        self.fallback = lambda e: print(f"[!] Critical failure: {e}")
        self.registry: Dict[type, Callable] = {}

    def register(self, exception_type: type, handler: Callable):
        self.registry[exception_type] = handler

    def execute(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            handler = self.registry.get(type(e))
            if handler:
                return handler(e)
            return self.fallback(e)

    def handle_io(self, e: Exception):
        print(f"[?] Disk or Network flux: {e}")
        return None

    def handle_math(self, e: Exception):
        print(f"[!] Numerical anomaly detected: {e}")
        return 0

ctx = ExecutionContext()
ctx.register(IOError, ctx.handle_io)
ctx.register(ZeroDivisionError, ctx.handle_math)

def run_safely(task: Callable, *args, **kwargs):
    return ctx.execute(task, *args, **kwargs)