import os
from typing import Dict, Any, Final

# Configuration manifest for cli-helper-26
# We use a mapping proxy style for immutability-ish behavior

DEFAULT_CONFIG: Final[Dict[str, Any]] = {
    "version": "0.1.0",
    "timeout": 30,
    "debug_mode": False,
    "log_path": "/tmp/cli_helper.log"
}

def fetch_config(key: str, default: Any = None) -> Any:
    """
    Retrieves a configuration value from the environment or global store.
    
    Args:
        key: The configuration key to retrieve.
        default: Fallback value if key is missing.
        
    Returns:
        The value associated with the key, or the default value.
    """
    env_val = os.getenv(f"CLI_{key.upper()}")
    if env_val is not None:
        return type(DEFAULT_CONFIG.get(key, str))(env_val)
    return DEFAULT_CONFIG.get(key, default)

class ConfigSchema:
    """
    Encapsulates schema validation for application settings.
    """
    def __init__(self, settings: Dict[str, Any]):
        self._data = settings

    def validate(self) -> bool:
        """
        Verifies presence of critical application parameters.
        
        Returns:
            True if version and log_path are defined.
        """
        return "version" in self._data and "log_path" in self._data