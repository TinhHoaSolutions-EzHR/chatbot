from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from typing import Optional

from models import Base


class EmbeddingModel(Base):
    __tablename__ = "embedding_model"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    description = Column(String)
    provider = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    deleted_at = Column(DateTime, default=None, nullable=True)


class EmbeddingModelRequest(BaseModel):
    name: str
    description: str
    provider: str


class EmbeddingModelResponse(BaseModel):
    id: int
    name: str
    description: str
    provider: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        from_attributes = True
