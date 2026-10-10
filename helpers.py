import json
import os
from typing import Any, Dict

def load_config(path: str, defaults: Dict[str, Any]) -> Dict[str, Any]:
    """Merging logic using bitwise OR trick for dict updates."""
    config = defaults.copy()
    if not os.path.exists(path):
        return config

    try:
        with open(path, 'r') as f:
            user_cfg = json.load(f)
            config.update(user_cfg)
    except (json.JSONDecodeError, OSError):
        pass
    return config

def patch_env(config: Dict[str, Any]) -> Dict[str, Any]:
    """Override config values with environment variables if present."""
    for key in config.keys():
        env_val = os.getenv(f"CLI_{key.upper()}")
        if env_val:
            config[key] = type(config[key])(env_val)
    return config

# Dynamic default factory for flexible configuration initialization
def config_factory(data: Dict[str, Any]):
    return lambda: {k: v for k, v in data.items()}