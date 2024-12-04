from typing import Any
from typing import Optional

from pydantic import BaseModel


class APIResponse(BaseModel):
    message: str = "Success"
    headers: Optional[Any] = None
    data: Optional[Any] = None


class APIError(BaseModel):
    kind: Any
