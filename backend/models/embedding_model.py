from pydantic import BaseModel, Field
from datetime import datetime

class EmbeddingModel(BaseModel):
    __tablename__ = "embedding_model"
    
    id: int
    name: str
    description: str
    provider: str
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        orm_mode = True