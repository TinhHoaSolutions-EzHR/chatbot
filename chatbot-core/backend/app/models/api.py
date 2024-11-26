from pydantic import BaseModel
from typing import Optional, Any

from app.utils.error_handler import ErrorCodesMappingNumber


class APIResponse(BaseModel):
    status_code: int = 200
    message: str = "Success"
    headers: Optional[Any] = None
    data: Optional[Any] = None


class APIError(BaseModel):
    kind: Any
