from pydantic import BaseModel
from typing import Optional

class ScraperRequest(BaseModel):
    pages: Optional[int] = None
    proxy: Optional[str] = None
