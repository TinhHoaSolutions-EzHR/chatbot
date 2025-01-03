from __future__ import annotations

import json
from datetime import datetime
from datetime import timezone
from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import TYPE_CHECKING
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from pydantic import model_validator
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import ChatSession
    from app.models import ChatMessage
    from app.models import User


class AgentType(str, Enum):
    """
    Enumeration of agent types.
    """

    SYSTEM = "system"
    USER = "user"


class Agent(Base):
    """
    Represents an agent is a user that can interact with the chatbot.
    Tracks chat sessions and messages that the agent is involved in.
    """

    __tablename__ = "agent"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid4
    )
    user_id: Mapped[Optional[UNIQUEIDENTIFIER]] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=True
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    prompt: Mapped[str] = mapped_column(String, nullable=True)
    agent_type: Mapped[AgentType] = mapped_column(
        SQLAlchemyEnum(AgentType, native_enum=False), nullable=False, default=AgentType.USER
    )
    is_visible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    uploaded_image_path: Mapped[Optional[str]] = mapped_column(String, nullable=True)
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
    chat_sessions: Mapped[List["ChatSession"]] = relationship("ChatSession", back_populates="agent")
    chat_messages: Mapped[List["ChatMessage"]] = relationship("ChatMessage", back_populates="agent")
    user: Mapped[Optional["User"]] = relationship("User", back_populates="agents")
    starter_messages: Mapped[List["StarterMessage"]] = relationship(
        "StarterMessage", back_populates="agent"
    )


class StarterMessage(Base):
    """
    Represents a starter message for an agent.
    Tracks the agent's starter message.
    """

    __tablename__ = "starter_message"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid4
    )
    agent_id: Mapped[Optional[UNIQUEIDENTIFIER]] = mapped_column(
        ForeignKey("agent.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    message: Mapped[str] = mapped_column(String, nullable=False)
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
    agent: Mapped[Optional["Agent"]] = relationship("Agent", back_populates="starter_messages")


class AgentRequest(BaseModel):
    """
    Pydantic model for creating a new agent.
    Defines the structure of agent data received from the client.
    """

    name: Optional[str] = Field(None, description="Agent name")
    prompt: Optional[str] = Field(None, description="Agent prompt")
    agent_type: AgentType = Field(AgentType.USER, description="Agent type")
    is_visible: bool = Field(True, description="Agent visibility")
    uploaded_image_path: Optional[str] = Field(None, description="Uploaded image id")
    starter_messages: Optional[List["StarterMessageRequest"]] = Field(
        default_factory=list, description="List of starter messages"
    )

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates that the provided value is a dictionary.

        Args:
            value (Dict[str, Any]): Value to validate.

        Returns:
            Dict[str, Any]: The validated value.
        """
        if isinstance(value, str):
            try:
                return cls(**json.loads(value))
            except json.JSONDecodeError as e:
                raise ValueError("Invalid JSON string provided") from e

        return value

    class Config:
        from_attributes = True


class StarterMessageRequest(BaseModel):
    """
    Pydantic model for creating a new starter message.
    Defines the structure of starter message data received from the client.
    """

    id: Optional[UUID] = Field(None, description="Starter message id")
    name: Optional[str] = Field(None, description="Starter message name")
    message: Optional[str] = Field(None, description="Starter message")

    class Config:
        from_attributes = True


class AgentResponse(BaseModel):
    """
    Pydantic model for returning an agent.
    Defines the structure of agent data returned to the client.
    """

    id: UUID = Field(..., description="Agent id")
    user_id: Optional[UUID] = Field(None, description="User id")
    name: str = Field(..., description="Agent name")
    prompt: str = Field(..., description="Agent prompt")
    agent_type: AgentType = Field(AgentType.USER, description="Agent type")
    is_visible: bool = Field(True, description="Agent visibility")
    uploaded_image_path: Optional[str] = Field(None, description="Uploaded image id")
    starter_messages: Optional[List["StarterMessageResponse"]] = Field(
        default_factory=list, description="List of starter messages"
    )
    created_at: datetime = Field(..., description="Created at timestamp")
    updated_at: datetime = Field(..., description="Updated at timestamp")
    deleted_at: Optional[datetime] = Field(None, description="Deleted at timestamp")

    class Config:
        from_attributes = True


class StarterMessageResponse(BaseModel):
    """
    Pydantic model for returning a starter message.
    Defines the structure of starter message data returned to the client.
    """

    id: UUID = Field(..., description="Starter message id")
    agent_id: UUID = Field(..., description="Agent id")
    name: str = Field(..., description="Starter message name")
    message: str = Field(..., description="Starter message")
    created_at: datetime = Field(..., description="Created at timestamp")
    updated_at: datetime = Field(..., description="Updated at timestamp")
    deleted_at: Optional[datetime] = Field(None, description="Deleted at timestamp")

    class Config:
        from_attributes = True
