import sys
from dataclasses import dataclass
from typing import Any, Callable, Dict

@dataclass
class CommandHandler:
    registry: Dict[str, Callable] = None

    def __post_init__(self):
        self.registry = {}

    def register(self, name: str):
        def decorator(func: Callable):
            self.registry[name] = func
            return func
        return decorator

    def execute(self, cmd: str, *args, **kwargs) -> Any:
        func = self.registry.get(cmd)
        if not func:
            raise ValueError(f"unknown command: {cmd}")
        return func(*args, **kwargs)

    @classmethod
    def bootstrap(cls, commands: Dict[str, Callable]):
        instance = cls()
        instance.registry.update(commands)
        return instance

def graceful_exit(code: int = 0):
    sys.stdout.write(f"\nterminating with code {code}\n")
    sys.exit(code)

def process_stream(data: str) -> str:
    return " ".join(data.strip().split()).upper()

if __name__ == "__main__":
    handler = CommandHandler()
    
    @handler.register("echo")
    def echo_cmd(text: str):
        return process_stream(text)

    try:
        print(handler.execute("echo", "  hello world  "))
    except Exception as e:
        print(f"execution error: {e}")
        graceful_exit(1)