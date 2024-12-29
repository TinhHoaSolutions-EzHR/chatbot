from __future__ import annotations

from datetime import datetime
from datetime import timezone
from enum import Enum
from typing import Any
from typing import Optional
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from app.models.base import Base


class LLMProviderType(str, Enum):
    """
    Enumeration of LLM provider types.
    """

    OPENAI = "openai"
    GEMINI = "gemini"
    COHERE = "cohere"


class LLMProvider(Base):
    """
    Represents an LLM provider that is stored in the database.
    Tracks and organizes LLM providers that are stored in the database.
    """

    __tablename__ = "llm_provider"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[LLMProviderType] = mapped_column(
        SQLAlchemyEnum(LLMProviderType, native_enum=False),
        nullable=False,
        default=LLMProviderType.OPENAI,
    )
    api_key: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    temperature: Mapped[float] = mapped_column(Float, nullable=False, default=0.7)
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
        if value < 0.0 or value > 1.0:
            raise ValueError("Temperature must be between 0.0 and 1.0.")

        return value


class LLMProviderRequest(BaseModel):
    """
    Pydantic model for LLM provider request.
    Defines the structure of LLM provider data received from the client.
    """

    name: LLMProviderType = Field(
        LLMProviderType.OPENAI, description="The name of the LLM provider."
    )
    api_key: Optional[str] = Field(
        None, description="The api key of the LLM provider.", exclude=True
    )
    temperature: float = Field(
        0.7, description="The temperature of the LLM provider.", ge=0.0, le=1.0
    )
    current_model: Optional[str] = Field(None, description="The current model of the LLM provider.")
    is_active: bool = Field(False, description="The active status of the LLM provider.")
    is_default_provider: bool = Field(False, description="The default status of the LLM provider.")

    class Config:
        from_attributes = True


class LLMProviderResponse(BaseModel):
    """
    Pydantic model for LLM provider response.
    Defines the structure of LLM provider data returned to the client.
    """

    id: UUID = Field(..., description="The unique identifier of the LLM provider.")
    name: LLMProviderType = Field(
        LLMProviderType.OPENAI, description="The name of the LLM provider."
    )
    temperature: float = Field(0.7, description="The temperature of the LLM provider.")
    current_model: str = Field(..., description="The current model of the LLM provider.")
    is_active: bool = Field(False, description="The active status of the LLM provider.")
    is_default_provider: bool = Field(False, description="The default status of the LLM provider.")
    created_at: datetime = Field(..., description="The creation timestamp of the LLM provider.")
    updated_at: datetime = Field(..., description="The update timestamp of the LLM provider.")
    deleted_at: Optional[datetime] = Field(
        None, description="The deletion timestamp of the LLM provider."
    )

    class Config:
        from_attributes = True
