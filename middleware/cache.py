import hashlib
import json
from datetime import datetime, timedelta
from typing import Optional

cache = {}

def get_cache_key(messages: list, model: str) -> str:
    content = json.dumps({"messages": messages, "model": model})
    return hashlib.md5(content.encode()).hexdigest()

def get_cached_response(key: str) -> Optional[dict]:
    cached = cache.get(key)
    if cached and cached.get("expires", datetime.min) > datetime.now():
        return cached.get("data")
    return None

def set_cached_response(key: str, value: dict, ttl_seconds: int = 3600):
    cache[key] = {"data": value, "expires": datetime.now() + timedelta(seconds=ttl_seconds)}
