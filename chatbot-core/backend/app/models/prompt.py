from __future__ import annotations

import json
from datetime import datetime
from datetime import timezone
from typing import Optional
from typing import TYPE_CHECKING
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from pydantic import model_validator
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import Agent


class Prompt(Base):
    """
    Represents a prompt in the chatbot system.
    Tracks answer is being constructed for the prompt.
    """

    __tablename__ = "prompt"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid4
    )
    agent_id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        ForeignKey("agent.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    task_prompt: Mapped[str] = mapped_column(Text, nullable=False)
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

    # Define relationships. We use the type hinting string to avoid circular imports.
    agent: Mapped[Agent] = relationship("Agent", back_populates="prompts")


class PromptRequest(BaseModel):
    """
    Pydantic model for prompt request.
    Defines the structure of folder data received from the client.
    """

    id: Optional[UUID] = Field(None, description="Prompt ID")
    name: Optional[str] = Field(None, description="Prompt name")
    description: Optional[str] = Field(None, description="Prompt description")
    system_prompt: Optional[str] = Field(None, description="System prompt")
    task_prompt: Optional[str] = Field(None, description="Task prompt")

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            try:
                return cls(**json.loads(value))
            except json.JSONDecodeError as e:
                raise ValueError("Invalid JSON string provided") from e
        return value

    class Config:
        from_attributes = True


class PromptResponse(BaseModel):
    """
    Pydantic model for prompt response.
    Defines the structure of prompt data sent to the client.
    """

    id: UUID = Field(..., description="Prompt ID")
    name: str = Field(..., description="Prompt name")
    description: Optional[str] = Field(None, description="Prompt description")
    system_prompt: str = Field(..., description="System prompt")
    task_prompt: str = Field(..., description="Task prompt")
    created_at: datetime = Field(..., description="Created at")
    updated_at: datetime = Field(..., description="Updated at")
    deleted_at: Optional[datetime] = Field(None, description="Deleted at")

    class Config:
        from_attributes = True
