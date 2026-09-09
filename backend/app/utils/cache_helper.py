from typing import Any
from app.extensions import cache


def clear_cache_pattern(pattern: str) -> None:
    backend: Any = getattr(cache, "cache", None)
    if backend is None:
        return

    redis_client = None
    for attr in ("_redis_client", "_write_client", "_read_client"):
        redis_client = getattr(backend, attr, None)
        if redis_client is not None:
            break

    if redis_client is None:
        return

    for key in redis_client.scan_iter(match=f"*{pattern}*"):
        redis_client.delete(key)
