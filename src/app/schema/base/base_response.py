from typing import Optional
from pydantic import BaseModel

class BaseResponseWrapper:
    def __init__(self, success: bool, data: dict = {}):
        self.success = success
        self.data = data
