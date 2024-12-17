from __future__ import annotations

from datetime import datetime
from datetime import timezone
from enum import Enum
from typing import Any
from typing import List
from typing import Optional
from typing import TYPE_CHECKING
from typing import Union
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator
from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import Agent
    from app.models import User
    from app.models import Prompt


class ChatMessageType(str, Enum):
    """
    Enumeration of message types in a chat session.
    """

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessageRequestType(str, Enum):
    """
    Enumeration of message types in a chat session.
    """

    NEW = "new"
    REGENERATE = "regenerate"
    EDIT = "edit"


class ChatMessageErrorType(str, Enum):
    """
    Enumeration of possible error types in a chat message.
    """

    SYSTEM_ERROR = "system_error"
    VALIDATION_ERROR = "validation_error"
    NETWORK_ERROR = "network_error"
    GENERATION_ERROR = "generation_error"


class ChatSessionSharedStatus(str, Enum):
    """
    Enumeration of chat session sharing statuses.
    """

    PUBLIC = "public"
    PRIVATE = "private"


CHAT_MESSAGES_ID = "chat_message.id"


class ChatSession(Base):
    """
    Represents a chat session between a user and an agent.
    Tracks conversation details, sharing status, and associated messages.
    """

    __tablename__ = "chat_session"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UNIQUEIDENTIFIER] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    agent_id: Mapped[Optional[UNIQUEIDENTIFIER]] = mapped_column(ForeignKey("agent.id"), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    shared_status: Mapped[ChatSessionSharedStatus] = mapped_column(
        SQLAlchemyEnum(ChatSessionSharedStatus, native_enum=False), default=ChatSessionSharedStatus.PRIVATE
    )
    current_alternate_model: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=lambda: datetime.now(timezone.utc)
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    # Define relationships. We use the type hinting string to avoid circular imports.
    user: Mapped["User"] = relationship("User", back_populates="chat_sessions", cascade="save-update, merge")
    agent: Mapped["Agent"] = relationship("Agent", back_populates="chat_sessions", cascade="save-update, merge")
    chat_messages: Mapped[List["ChatMessage"]] = relationship(
        "ChatMessage", back_populates="chat_session", cascade="all, delete-orphan", lazy="dynamic"
    )


class ChatMessage(Base):
    """
    Represents an individual message within a chat session.
    Tracks message content, type, and associated metadata.
    """

    __tablename__ = "chat_message"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UNIQUEIDENTIFIER] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    chat_session_id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        ForeignKey("chat_session.id", ondelete="CASCADE"), nullable=False
    )
    agent_id: Mapped[UNIQUEIDENTIFIER] = mapped_column(ForeignKey("agent.id"), nullable=False)
    parent_message_id: Mapped[Optional[UNIQUEIDENTIFIER]] = mapped_column(ForeignKey(CHAT_MESSAGES_ID), nullable=True)
    child_message_id: Mapped[Optional[UNIQUEIDENTIFIER]] = mapped_column(ForeignKey(CHAT_MESSAGES_ID), nullable=True)
    message: Mapped[str] = mapped_column(Text)
    prompt_id: Mapped[Optional[UNIQUEIDENTIFIER]] = mapped_column(ForeignKey("prompt.id"), nullable=True)
    token_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    message_type: Mapped[ChatMessageType] = mapped_column(
        SQLAlchemyEnum(ChatMessageType, native_enum=False), nullable=False
    )
    error_type: Mapped[Optional[ChatMessageErrorType]] = mapped_column(
        SQLAlchemyEnum(ChatMessageErrorType), nullable=True
    )
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=lambda: datetime.now(timezone.utc)
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    # Define relationships. We use the type hinting string to avoid circular imports.
    user: Mapped["User"] = relationship("User", back_populates="chat_messages")
    chat_session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="chat_messages")
    agent: Mapped[Optional["Agent"]] = relationship("Agent", back_populates="chat_messages")
    prompt: Mapped[Optional["Prompt"]] = relationship("Prompt", back_populates="chat_messages")

    @validates("token_count")
    def validate_token_count(self, key: Any, token_count: int) -> Union[int, None]:
        """
        Validate token count.

        Args:
            key (Any): Key.
            token_count (int): Token count.
        """
        if token_count < 0:
            raise ValueError("Token count must be greater than or equal to zero.")
        return token_count


class ChatMessageRequest(BaseModel):
    """
    Pydantic model for creating a new chat message.
    Provides validation for incoming chat message requests.
    """

    id: Optional[UUID] = Field(None, description="Chat message id")
    agent_id: Optional[UUID] = Field(None, description="Current agent id")
    parent_message_id: Optional[UUID] = Field(None, description="Parent message id")
    child_message_id: Optional[UUID] = Field(None, description="Child message id")
    message: Optional[str] = Field(None, description="Message text", min_length=1, max_length=10000)
    prompt_id: Optional[UUID] = Field(None, description="Prompt id")
    request_type: ChatMessageRequestType = Field(description="Request type", default=ChatMessageRequestType.NEW)

    class Config:
        from_attributes = True


class ChatMessageResponse(BaseModel):
    """
    Pydantic model for chat message response.
    Defines the structure of chat message data returned to the client.
    """

    id: UUID = Field(..., description="Chat message id")
    user_id: UUID = Field(..., description="User id")
    chat_session_id: UUID = Field(..., description="Chat session id")
    message: str = Field(..., description="Message text")
    message_type: ChatMessageType = Field(..., description="Message type")
    parent_message_id: Optional[UUID] = Field(None, description="Parent message id")
    child_message_id: Optional[UUID] = Field(None, description="Latest child message id")
    created_at: datetime = Field(..., description="Created at timestamp")
    updated_at: datetime = Field(..., description="Updated at timestamp")

    class Config:
        from_attributes = True


class ChatSessionRequest(BaseModel):
    """
    Pydantic model for creating a new chat session.
    Provides validation for incoming chat session requests.
    """

    agent_id: Optional[str] = Field(None, description="Agent id of the chat session")
    description: Optional[str] = Field(None, max_length=255, description="Description (Name) of the chat session")
    shared_status: ChatSessionSharedStatus = Field(ChatSessionSharedStatus.PRIVATE, description="Shared status")
    current_alternate_model: Optional[str] = Field(None, description="Current alternate model")

    @field_validator("description")
    def validate_description(cls, value: Optional[str]) -> Optional[str]:
        """
        Validate description.

        Args:
            value (Optional[str]): Description.
        """
        if value and len(value) > 255:
            raise ValueError("Description must be 255 characters or less")
        return value

    class Config:
        from_attributes = True


class ChatSessionResponse(BaseModel):
    """
    Pydantic model for chat session response.
    Defines the structure of chat session data returned to the client.
    """

    id: UUID = Field(..., description="Chat session id")
    description: Optional[str] = Field(None, description="Description (Name) of the chat session")
    user_id: UUID = Field(..., description="User id of the chat session")
    agent_id: Optional[UUID] = Field(None, description="Agent id of the chat session")
    messages: Optional[List[ChatMessageResponse]] = Field(None, description="Chat messages")
    shared_status: ChatSessionSharedStatus = Field(ChatSessionSharedStatus.PRIVATE, description="Shared status")
    created_at: datetime = Field(..., description="Created at timestamp")
    updated_at: datetime = Field(..., description="Updated at timestamp")

    class Config:
        from_attributes = True
