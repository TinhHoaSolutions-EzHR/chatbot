from pydantic import BaseModel

class APIError(BaseModel):
    detail: str