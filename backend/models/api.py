from pydantic import BaseModel
from typing import Optional, Any

class APIResponse(BaseModel):
    status_code: int = 200
    message: str = "Success"
    headers: Optional[Any] = None
    data: Optional[Any] = None
    pagination: Optional[Any] = None