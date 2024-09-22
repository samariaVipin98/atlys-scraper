from datetime import datetime, timedelta
import os
import time
from functools import wraps
from typing import Optional

import bcrypt
from jose import JWTError, jwt

from schema.auth.auth_request import TokenData

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

def get_password_hash(password):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')

def check_password(provided_password, hashed_password):
    provided_password_bytes = provided_password
    return bcrypt.checkpw(provided_password_bytes, hashed_password)


def create_access_token(username: str, expires_delta: Optional[timedelta] = None):
    to_encode = {"username": username}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("JWT_ALGORITHM"))
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=[os.getenv("JWT_ALGORITHM")])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data
