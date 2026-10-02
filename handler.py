import sys
from typing import Callable, Any, Dict

class CommandRegistry:
    def __init__(self):
        self._actions: Dict[str, Callable] = {}

    def register(self, cmd: str):
        def decorator(func: Callable):
            self._actions[cmd] = func
            return func
        return decorator

    def execute(self, cmd: str, *args: Any, **kwargs: Any) -> Any:
        return self._actions.get(cmd, self._default)(*args, **kwargs)

    def _default(self, *_, **__):
        return "Command not recognized"

registry = CommandRegistry()

@registry.register("ping")
def ping(*_):
    return "pong"

@registry.register("echo")
def echo(msg: str = ""):
    return msg

def run_handler(cmd_str: str):
    parts = cmd_str.split(maxsplit=1)
    cmd = parts[0]
    arg = parts[1] if len(parts) > 1 else None
    return registry.execute(cmd, arg)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(run_handler(" ".join(sys.argv[1:])))