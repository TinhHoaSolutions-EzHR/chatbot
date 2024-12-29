from __future__ import annotations

from datetime import datetime
from datetime import timezone
from enum import Enum
from typing import Optional
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from app.models.base import Base


class EmbeddingProviderType(Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    COHERE = "cohere"


class EmbeddingProvider(Base):
    """
    Represents an embedding provider that is used for embedding text.
    Tracks and organizes embedding providers that are stored in the database.
    """

    __tablename__ = "embedding_model"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[EmbeddingProviderType] = mapped_column(
        SQLAlchemyEnum(EmbeddingProviderType, native_enum=False),
        default=EmbeddingProviderType.OPENAI,
    )
    api_key: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    dimensions: Mapped[int] = mapped_column(Integer, nullable=False)
    embed_batch_size: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    current_model: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_default_provider: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
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


class EmbeddingProviderRequest(BaseModel):
    """
    Pydantic model for embedding provider request.
    Defines the structure of embedding provider data received from the client.
    """

    name: EmbeddingProviderType = Field(
        EmbeddingProviderType.OPENAI, description="The name of the embedding provider"
    )
    api_key: Optional[str] = Field(
        None, description="API key for the embedding provider", exclude=True
    )
    dimensions: Optional[int] = Field(
        None, description="Number of dimensions in the embedding model"
    )
    embed_batch_size: Optional[int] = Field(10, description="Batch size for the embedding model")
    current_model: Optional[str] = Field(
        None, description="The current model of the embedding provider."
    )
    is_active: bool = Field(False, description="The active status of the embedding provider.")
    is_default_provider: bool = Field(
        False, description="The default status of the embedding provider."
    )

    class Config:
        from_attributes = True


class EmbeddingProviderResponse(BaseModel):
    """
    Pydantic model for embedding provider response.
    Defines the structure of embedding provider data returned to the client.
    """

    id: UUID = Field(..., description="The unique identifier of the embedding provider")
    name: EmbeddingProviderType = Field(
        EmbeddingProviderType.OPENAI, description="The name of the embedding provider"
    )
    dimensions: Optional[int] = Field(
        None, description="Number of dimensions in the embedding model"
    )
    embed_batch_size: int = Field(10, description="Batch size for the embedding model")
    current_model: str = Field(..., description="The current model of the embedding provider.")
    is_active: bool = Field(False, description="The active status of the embedding provider.")
    is_default_provider: bool = Field(
        False, description="The default status of the embedding provider."
    )
    created_at: datetime = Field(
        ..., description="The creation timestamp of the embedding provider."
    )
    updated_at: datetime = Field(..., description="The update timestamp of the embedding provider.")
    deleted_at: Optional[datetime] = Field(
        None, description="The deletion timestamp of the embedding provider."
    )

    class Config:
        from_attributes = True
