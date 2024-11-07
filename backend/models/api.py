from pydantic import BaseModel
from typing import Optional, Any

from utils.error_handler import ErrorCodesMappingNumber


class APIResponse(BaseModel):
    message: str = "Success"
    headers: Optional[Any] = None
    data: Optional[Any] = None


class APIError(BaseModel):
    kind: Any
