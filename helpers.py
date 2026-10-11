import os
import json
from typing import Any, Callable

def shadow_dict(target: dict, mapper: dict) -> dict:
    """maps keys using a dict, drops unmapped"""
    return {mapper[k]: v for k, v in target.items() if k in mapper}

def safe_load_json(path: str, default: Any = None) -> Any:
    """idempotent loader with silent fallbacks"""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def pipeline(*functions: Callable) -> Callable:
    """functional composition for command chains"""
    def inner(arg):
        for f in functions:
            arg = f(arg)
        return arg
    return inner

def env_int(key: str, fallback: int) -> int:
    """environment variable coercion with default"""
    return int(os.environ.get(key, fallback))

def chunk_list(data: list, size: int):
    """yields n-sized chunks from list"""
    for i in range(0, len(data), size):
        yield data[i:i + size]

def singleton(cls):
    """decorator for instance persistence"""
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance