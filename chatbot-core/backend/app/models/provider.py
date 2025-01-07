from __future__ import annotations

from datetime import datetime
from datetime import timezone
from enum import Enum
from typing import Any
from typing import List
from typing import Optional
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import LargeBinary
from sqlalchemy import String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from app.models.base import Base


class ProviderType(Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    COHERE = "cohere"


class BaseProvider(Base):
    """
    SQLAlchemy base class for all providers, including Embedding and LLM providers.
    """

    __abstract__ = True

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[ProviderType] = mapped_column(
        SQLAlchemyEnum(ProviderType, native_enum=False),
        default=ProviderType.OPENAI,
    )
    api_key: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)
    models: Mapped[str] = mapped_column(String, nullable=True)
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


class EmbeddingProvider(BaseProvider):
    """
    Represents an embedding provider that is used for embedding text.
    Tracks and organizes embedding providers that are stored in the database.
    """

    __tablename__ = "embedding_provider"

    dimensions: Mapped[int] = mapped_column(Integer, nullable=False)
    embed_batch_size: Mapped[int] = mapped_column(Integer, nullable=False, default=10)

    @validates("dimensions", "embed_batch_size")
    def validate_positive(self, key: Any, value: int) -> int:
        """
        Validate that the value of the key is positive.

        Args:
            key (Any): The key to validate.
            value (int): The value to validate.

        Returns:
            int: The validated value.
        """
        # Value of the key must be positive
        if value < 0:
            raise ValueError(f"{key} must be positive.")

        return value


class LLMProvider(BaseProvider):
    """
    Represents an LLM provider that is stored in the database.
    Tracks and organizes LLM providers that are stored in the database.
    """

    __tablename__ = "llm_provider"

    temperature: Mapped[float] = mapped_column(Float, nullable=False, default=0.7)

    @validates("temperature")
    def validate_temperature(self, key: Any, value: float) -> float:
        """
        Validate that the temperature is between 0.0 and 1.0.

        Args:
            key (Any): The key of the attribute.
            value (float): The value of the attribute.

        Returns:
            float: The validated temperature
        """
        if value < 0.0:
            raise ValueError("Temperature must be greater than or equal to 0.0.")
        if (self.name == ProviderType.COHERE or self.name == ProviderType.OPENAI) and value > 1.0:
            raise ValueError("Temperature must be less than or equal to 1.0.")
        if self.name == ProviderType.GEMINI and value > 2.0:
            raise ValueError("Temperature must be less than or equal to 2.0.")

        return value


class BaseProviderRequest(BaseModel):
    """
    Pydantic model for provider request.
    Defines the structure of provider data received from the client.
    """

    api_key: Optional[str] = Field(None, description="API key for the provider")
    models: Optional[List[str]] = Field(
        default_factory=list, description="The models of the provider."
    )
    current_model: Optional[str] = Field(None, description="The current model of the provider.")
    is_active: bool = Field(False, description="The active status of the provider.")
    is_default_provider: bool = Field(False, description="The default status of the provider.")

    class Config:
        from_attributes = True


class BaseProviderResponse(BaseModel):
    """
    Pydantic model for provider response.
    Defines the structure of provider data returned to the client.
    """

    id: UUID = Field(..., description="The unique identifier of the provider")
    name: ProviderType = Field(..., description="The name of the provider")
    api_key: Optional[str] = Field(None, description="API key for the provider", exclude=True)
    models: List[str] = Field(..., description="The models of the provider.")
    current_model: str = Field(..., description="The current model of the provider.")
    is_active: bool = Field(False, description="The active status of the provider.")
    is_default_provider: bool = Field(False, description="The default status of the provider.")
    created_at: datetime = Field(..., description="The creation timestamp of the provider.")
    updated_at: datetime = Field(..., description="The update timestamp of the provider.")
    deleted_at: Optional[datetime] = Field(
        None, description="The deletion timestamp of the provider."
    )

    class Config:
        from_attributes = True


class EmbeddingProviderRequest(BaseProviderRequest):
    """
    Pydantic model for embedding provider request.
    Defines the structure of embedding provider data received from the client.
    """

    dimensions: Optional[int] = Field(
        None, description="Number of dimensions in the embedding model", gt=0
    )
    embed_batch_size: Optional[int] = Field(
        10, description="Batch size for the embedding model", gt=0
    )


class EmbeddingProviderResponse(BaseProviderResponse):
    """
    Pydantic model for embedding provider response.
    Defines the structure of embedding provider data returned to the client.
    """

    dimensions: Optional[int] = Field(
        None, description="Number of dimensions in the embedding model"
    )
    embed_batch_size: int = Field(..., description="Batch size for the embedding model")


class LLMProviderRequest(BaseProviderRequest):
    """
    Pydantic model for LLM provider request.
    Defines the structure of LLM provider data received from the client.
    """

    temperature: float = Field(
        0.7, description="The temperature of the LLM provider.", ge=0.0, le=1.0
    )

    @field_validator("temperature")
    def validate_temperature(cls, value: Optional[float]) -> Optional[float]:
        """
        Validate that the temperature is between 0.0 and 1.0.

        Args:
            value (Optional[float]): The temperature value to validate.

        Returns:
            Optional[float]: The validated temperature value.
        """
        if value and (value < 0.0 or value > 2.0):
            raise ValueError("Temperature must be between 0.0 and 2.0.")


class LLMProviderResponse(BaseProviderResponse):
    """
    Pydantic model for LLM provider response.
    Defines the structure of LLM provider data returned to the client.
    """

    temperature: float = Field(..., description="The temperature of the LLM provider.")
