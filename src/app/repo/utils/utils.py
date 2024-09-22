import time
from functools import wraps

cache = {}

def retry(max_retries: int, delay: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for _ in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

def cache_get(key: str) -> float:
    return cache.get(key, None)

def cache_set(key: str, value: float):
    cache[key] = value
