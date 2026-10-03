from typing import Any, Dict, Callable, Optional

class CommandHandler:
    """Dynamic command execution dispatcher for cli-helper-26."""

    def __init__(self) -> None:
        self._registry: Dict[str, Callable[[Any], Any]] = {}

    def register(self, name: str, func: Callable[[Any], Any]) -> None:
        """Register a function under a specific command key."""
        self._registry[name] = func

    def execute(self, name: str, data: Any = None) -> Optional[Any]:
        """Invoke registered command or return None if missing."""
        action = self._registry.get(name)
        if action:
            return action(data)
        return None

    def list_commands(self) -> list[str]:
        """Return available registered commands."""
        return list(self._registry.keys())

    def __call__(self, name: str, *args: Any, **kwargs: Any) -> Any:
        """Syntactic sugar for handler.execute."""
        cmd = self._registry.get(name)
        if callable(cmd):
            return cmd(*args, **kwargs)
        raise ValueError(f"Command '{name}' is not registered.")