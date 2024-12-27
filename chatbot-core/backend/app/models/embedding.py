from __future__ import annotations

from datetime import datetime
from datetime import timezone
from typing import Optional
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from app.models.base import Base


class EmbeddingModel(Base):
    """
    Represents an embedding model that is used for embedding text.
    Tracks and organizes embedding models that are stored in the database.
    """

    __tablename__ = "embedding_model"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    provider: Mapped[str] = mapped_column(String, nullable=False)
    model_type: Mapped[str] = mapped_column(String, nullable=False)
    api_key: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    base_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    dimensions: Mapped[int] = mapped_column(Integer, nullable=False)
    max_input_length: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    batch_size: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_active: Mapped[bool] = mapped_column(Integer, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )


class EmbeddingModelRequest(BaseModel):
    """
    Pydantic model for embedding model request.
    Defines the structure of embedding model data received from the client.
    """

    name: Optional[str] = Field(None, description="Folder name")
    provider: Optional[str] = Field(None, description="Provider of the embedding model")
    model_type: Optional[str] = Field(None, description="Type of the embedding model")
    api_key: Optional[str] = Field(None, description="API key for the embedding model")
    base_url: Optional[str] = Field(None, description="Base URL for the embedding model")
    dimensions: Optional[int] = Field(
        None, description="Number of dimensions in the embedding model"
    )
    max_input_length: Optional[int] = Field(
        None, description="Maximum input length for the embedding model"
    )
    batch_size: int = Field(1, description="Batch size for the embedding model")
    is_active: bool = Field(False, description="Whether the embedding model is active")

    class Config:
        from_attributes = True


class EmbeddingModelResponse(BaseModel):
    """
    Pydantic model for embedding model response.
    Defines the structure of embedding model data returned to the client.
    """

    id: UUID = Field(..., description="Folder ID")
    name: str = Field(..., description="Folder name")
    provider: str = Field(..., description="Provider of the embedding model")
    model_type: str = Field(..., description="Type of the embedding model")
    api_key: Optional[str] = Field(None, description="API key for the embedding model")
    base_url: Optional[str] = Field(None, description="Base URL for the embedding model")
    dimensions: int = Field(..., description="Number of dimensions in the embedding model")
    max_input_length: Optional[int] = Field(
        None, description="Maximum input length for the embedding model"
    )
    batch_size: int = Field(1, description="Batch size for the embedding model")
    is_active: bool = Field(False, description="Whether the embedding model is active")
    created_at: datetime = Field(..., description="Time when the embedding model was created")
    updated_at: datetime = Field(..., description="Time when the embedding model was last updated")
    deleted_at: Optional[datetime] = Field(
        None, description="Time when the embedding model was deleted"
    )

    class Config:
        from_attributes = True
