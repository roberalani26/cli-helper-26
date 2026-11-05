import os
import json
import logging
from pathlib import Path

class ConfigLoader:
    def __init__(self, path: str = 'settings.json'):
        self.path = Path(path)
        self.data = {}

    def load(self):
        try:
            if not self.path.exists():
                raise FileNotFoundError(f"Config missing: {self.path}")
            
            with open(self.path, 'r') as f:
                self.data = json.load(f)
                
        except (json.JSONDecodeError, PermissionError, FileNotFoundError) as e:
            self._handle_error(e)
        return self.data

    def _handle_error(self, err):
        fallback = {'theme': 'dark', 'retries': 3}
        logging.error(f"Configuration failure: {err}. Using default state.")
        self.data = fallback

    def get(self, key, default=None):
        return self.data.get(key, default)

    def validate_env(self):
        if 'API_KEY' not in os.environ:
            raise EnvironmentError("Critical: API_KEY missing from system env")
        return True