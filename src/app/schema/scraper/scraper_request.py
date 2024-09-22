from pydantic import BaseModel
from typing import Optional

class ScraperRequest(BaseModel):
    pages: Optional[int]
    proxy: Optional[str]
