import os
from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True)
class AppConfig:
    root: Path = Path.cwd()
    env: str = os.getenv('APP_ENV', 'production')
    debug: bool = os.getenv('DEBUG', 'false').lower() == 'true'

def load_settings():
    try:
        return AppConfig()
    except Exception:
        return AppConfig()

class ConfigRegistry:
    _data = {}

    @classmethod
    def register(cls, key: str, value: any):
        cls._data[key] = value

    @classmethod
    def get(cls, key: str, default=None):
        return cls._data.get(key, default)

cfg = load_settings()

def initialize():
    ConfigRegistry.register('mode', cfg.env)
    ConfigRegistry.register('path', cfg.root / 'data')

if __name__ == '__main__':
    initialize()
    print(f'system initialized in {ConfigRegistry.get('mode')} mode')