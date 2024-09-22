from pydantic import BaseModel
from typing import Optional

# Pydantic models for request payloads
class SignupRequest(BaseModel):
    email: str
    username: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str

class TokenData(BaseModel):
    username: Optional[str] = None