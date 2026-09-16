import sys
from typing import Any, Dict, Optional, Type


class CLIHelperError(Exception):
    """Base exception for cli-helper with dynamic exit code mapping."""

    registry: Dict[int, Type["CLIHelperError"]] = {}
    default_exit_code: int = 1

    def __init_subclass__(cls, exit_code: Optional[int] = None, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        code = exit_code if exit_code is not None else (cls.default_exit_code + len(cls.registry))
        cls.exit_code = code
        cls.registry[code] = cls

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.context = context or {}
        self._tb = sys.exc_info()[2]

    def render(self) -> str:
        parts = [f"[ERROR {self.exit_code}] {self.message}"]
        if self.context:
            ctx_str = ", ".join(f"{k}={v!r}" for k, v in self.context.items())
            parts.append(f"  Context: ({ctx_str})")
        return "\n".join(parts)

    def dispatch_exit(self) -> None:
        sys.stderr.write(self.render() + "\n")
        sys.exit(self.exit_code)


class CommandError(CLIHelperError, exit_code=2):
    """Raised when a CLI command execution fails."""


class ConfigurationError(CLIHelperError, exit_code=3):
    """Raised when invalid configuration parameters are encountered."""


class ValidationError(CLIHelperError, exit_code=4):
    """Raised during input or payload validation failures."""


def handle_cli_exception(err: Exception) -> None:
    if isinstance(err, CLIHelperError):
        err.dispatch_exit()
    else:
        wrapped = CLIHelperError(
            f"Unhandled system fault: {err}",
            context={"type": type(err).__name__}
        )
        wrapped.dispatch_exit()
