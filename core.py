import os
from pathlib import Path
from typing import Any, Dict

class CliCore:
    def __init__(self, workspace: str = "."):
        self.root = Path(workspace).resolve()
        self.registry: Dict[str, Any] = {}

    def __call__(self, key: str, func: callable) -> None:
        self.registry[key] = func

    def dispatch(self, cmd: str, *args, **kwargs) -> Any:
        return self.registry.get(cmd, lambda *a, **k: None)(*args, **kwargs)

    def cleanup(self, pattern: str = "*.tmp"):
        for path in self.root.rglob(pattern):
            try:
                path.unlink()
            except OSError:
                pass

    def reorganize(self, structure: Dict[str, str]):
        for src, dest in structure.items():
            src_path = self.root / src
            if src_path.exists():
                dest_path = self.root / dest
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                src_path.rename(dest_path)

if __name__ == "__main__":
    cli = CliCore()
    cli.cleanup()
    print("system state optimized")