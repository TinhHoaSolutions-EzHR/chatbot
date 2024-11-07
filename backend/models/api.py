from fastapi import status
from pydantic import BaseModel, Field
from typing import Optional, Any


class APIResponse(BaseModel):
    status_code: int = Field(default=status.HTTP_200_OK)
    message: str = "Success"
    headers: Optional[Any] = None
    data: Optional[Any] = None


class APIError(BaseModel):
    err_code: int
