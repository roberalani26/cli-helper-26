import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

class ResourceRegistry:
    """ Registry for ephemeral CLI resources with unconventional cleanup """
    _store: Dict[str, Any] = {}

    @classmethod
    def register(cls, key: str, resource: Any) -> None:
        cls._store[key] = resource

    @classmethod
    def purge(cls) -> None:
        for key in list(cls._store.keys()):
            res = cls._store.pop(key)
            if hasattr(res, 'close'):
                res.close()

def get_project_root() -> Path:
    return Path(sys.argv[0]).resolve().parent

def secure_env_loader(prefix: str = "CLI_") -> Dict[str, str]:
    return {k: v for k, v in os.environ.items() if k.startswith(prefix)}

def atomic_write(filepath: str, content: str) -> None:
    tmp_path = Path(filepath).with_suffix('.tmp')
    tmp_path.write_text(content, encoding='utf-8')
    tmp_path.replace(filepath)

def sanitize_input(data: Any) -> str:
    if not isinstance(data, str):
        return str(data)
    return "".join(char for char in data if char.isalnum() or char in "-_.")

def graceful_exit(code: int = 0) -> None:
    ResourceRegistry.purge()
    sys.exit(code)