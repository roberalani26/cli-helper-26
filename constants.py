import os
from pathlib import Path
from typing import Final, Dict, Any

# Configuration defaults and environment paths
BASE_DIR: Final[Path] = Path(__file__).resolve().parent
LOG_LEVEL: Final[str] = os.getenv('CLI_LOG_LEVEL', 'INFO')
TIMEOUT_SECONDS: Final[int] = int(os.getenv('CLI_TIMEOUT', '30'))

# Terminal style constants for CLI output decoration
COLORS: Final[Dict[str, str]] = {
    'HEADER': '\033[95m',
    'BLUE': '\033[94m',
    'GREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
}

# Application lifecycle states
STATE_MAP: Final[Dict[str, int]] = {
    'INITIALIZED': 0,
    'RUNNING': 1,
    'PAUSED': 2,
    'SHUTDOWN': 3,
}

# Common validation regex patterns
VALIDATION_SCHEMAS: Final[Dict[str, str]] = {
    'email': r'^[a-z0-9]+@[a-z0-9]+\.[a-z]{2,}$',
    'version': r'\d+\.\d+\.\d+',
}

def get_app_identity() -> Dict[str, Any]:
    """Returns the current identity mapping for context."""
    return {
        'project': 'cli-helper-26',
        'version': '1.0.0',
        'debug_mode': LOG_LEVEL == 'DEBUG'
    }