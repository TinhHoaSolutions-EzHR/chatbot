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


class LLMModel(Base):
    """
    Represents an llm model that is used for generating responses.
    Tracks and organizes llm models that are stored in the database.
    """

    __tablename__ = "llm_model"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    provider: Mapped[str] = mapped_column(String, nullable=False)
    model_type: Mapped[str] = mapped_column(String, nullable=False)
    api_key: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    base_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    context_length: Mapped[int] = mapped_column(Integer, nullable=False)
    max_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    temperature: Mapped[float] = mapped_column(Integer, nullable=False, default=0.7)
    top_p: Mapped[float] = mapped_column(Integer, nullable=False, default=1.0)
    frequency_penalty: Mapped[float] = mapped_column(Integer, nullable=False, default=0.0)
    presence_penalty: Mapped[float] = mapped_column(Integer, nullable=False, default=0.0)
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


class LLMModelRequest(BaseModel):
    """
    Pydantic model for llm model request.
    Defines the structure of llm model data received from the client.
    """

    name: Optional[str] = Field(None, description="The name of the llm model.")
    provider: Optional[str] = Field(None, description="The provider of the llm model.")
    model_type: Optional[str] = Field(None, description="The type of the llm model.")
    api_key: Optional[str] = Field(None, description="The api key of the llm model.")
    base_url: Optional[str] = Field(None, description="The base url of the llm model.")
    context_length: Optional[int] = Field(None, description="The context length of the llm model.")
    max_tokens: Optional[int] = Field(None, description="The max tokens of the llm model.")
    temperature: float = Field(0.7, description="The temperature of the llm model.")
    top_p: float = Field(1.0, description="The top p of the llm model.")
    frequency_penalty: float = Field(0.0, description="The frequency penalty of the llm model.")
    presence_penalty: float = Field(0.0, description="The presence penalty of the llm model.")
    is_active: bool = Field(False, description="The active status of the llm model.")

    class Config:
        from_attributes = True


class LLMModelResponse(BaseModel):
    """
    Pydantic model for llm model response.
    Defines the structure of llm model data returned to the client.
    """

    id: UUID = Field(..., description="The unique identifier of the llm model.")
    name: str = Field(..., description="The name of the llm model.")
    provider: str = Field(..., description="The provider of the llm model.")
    model_type: str = Field(..., description="The type of the llm model.")
    api_key: Optional[str] = Field(None, description="The api key of the llm model.")
    base_url: Optional[str] = Field(None, description="The base url of the llm model.")
    context_length: int = Field(..., description="The context length of the llm model.")
    max_tokens: int = Field(..., description="The max tokens of the llm model.")
    temperature: float = Field(0.7, description="The temperature of the llm model.")
    top_p: float = Field(1.0, description="The top p of the llm model.")
    frequency_penalty: float = Field(0.0, description="The frequency penalty of the llm model.")
    presence_penalty: float = Field(0.0, description="The presence penalty of the llm model.")
    is_active: bool = Field(False, description="The active status of the llm model.")
    created_at: datetime = Field(..., description="The creation timestamp of the llm model.")
    updated_at: datetime = Field(..., description="The update timestamp of the llm model.")
    deleted_at: Optional[datetime] = Field(
        None, description="The deletion timestamp of the llm model."
    )

    class Config:
        from_attributes = True
