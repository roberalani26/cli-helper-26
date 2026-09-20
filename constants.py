import os
import sys
from typing import Final, Any

class ConfigError(Exception):
    """Custom sentinel for configuration failures."""
    pass

def get_env_variable(key: str, fallback: Any = None) -> Any:
    try:
        return os.environ[key]
    except KeyError:
        if fallback is not None:
            return fallback
        raise ConfigError(f"Required environment variable '{key}' is missing")

def validate_system_constraints():
    if sys.version_info < (3, 8):
        raise RuntimeError("Python 3.8+ required for operational stability")
    if not os.access(os.getcwd(), os.W_OK):
        raise PermissionError("Working directory is not writable")

MAX_RETRIES: Final[int] = 3
TIMEOUT_SECONDS: Final[float] = 30.5

# Dynamic registry of critical constants loaded at runtime
# to ensure early-fail during edge case startup
RUNTIME_CONSTANTS = {
    "retries": get_env_variable("CLI_RETRIES", MAX_RETRIES),
    "timeout": get_env_variable("CLI_TIMEOUT", TIMEOUT_SECONDS),
    "environment": get_env_variable("APP_ENV", "production")
}

try:
    validate_system_constraints()
except (RuntimeError, PermissionError) as e:
    sys.stderr.write(f"[FATAL] System constraints not met: {e}\n")
    sys.exit(1)