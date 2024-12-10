from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List
from typing import Optional
from typing import TYPE_CHECKING
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from sqlalchemy import Boolean
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

from app.models.base import Base
# from app.models.prompt import Prompt
# from app.models.user import User

if TYPE_CHECKING:
    from app.models import Agent


class MessageType(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatSessionSharedStatus(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"


CHAT_MESSAGES_ID = "chat_messages.id"


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    user_id: Mapped[UNIQUEIDENTIFIER] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    agent_id: Mapped[UNIQUEIDENTIFIER] = mapped_column(ForeignKey("agents.id"), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    one_shot: Mapped[bool] = mapped_column(Boolean, default=False)
    shared_status: Mapped[ChatSessionSharedStatus] = mapped_column(
        SQLAlchemyEnum(ChatSessionSharedStatus, native_enum=False), default=ChatSessionSharedStatus.PRIVATE
    )
    current_alternate_model: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    # user: Mapped["User"] = relationship("User", back_populates="chat_sessions")
    agent: Mapped["Agent"] = relationship("Agent", back_populates="chat_sessions")
    chat_messages: Mapped[List["ChatMessage"]] = relationship(
        "ChatMessage", back_populates="chat_session", lazy="selectin"
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    chat_session_id: Mapped[UNIQUEIDENTIFIER] = mapped_column(ForeignKey("chat_sessions.id", ondelete="CASCADE"))
    alternate_agent_id: Mapped[Optional[UNIQUEIDENTIFIER]] = mapped_column(ForeignKey("agents.id"), nullable=True)
    parent_message_id: Mapped[Optional[UNIQUEIDENTIFIER]] = mapped_column(ForeignKey(CHAT_MESSAGES_ID), nullable=True)
    latest_child_message_id: Mapped[Optional[UNIQUEIDENTIFIER]] = mapped_column(
        ForeignKey(CHAT_MESSAGES_ID), nullable=True
    )
    message: Mapped[str] = mapped_column(Text)
    prompt_id: Mapped[Optional[UNIQUEIDENTIFIER]] = mapped_column(ForeignKey("prompts.id"), nullable=True)
    token_count: Mapped[int] = mapped_column(Integer)
    message_type: Mapped[MessageType] = mapped_column(SQLAlchemyEnum(MessageType, native_enum=False), nullable=False)
    error: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    chat_session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="chat_messages")
    agent: Mapped["Agent"] = relationship("Agent", back_populates="chat_messages")
    # prompt: Mapped["Prompt"] = relationship("Prompt", back_populates="chat_messages")
    # chat_message_feedbacks: Mapped[List["ChatMessageFeedback"]] = relationship(
    #     "ChatMessageFeedback", back_populates="chat_message"
    # )
    # parent_message: Mapped["ChatMessage"] = relationship(
    #     "ChatMessage", remote_side=[id], foreign_keys=[parent_message_id], back_populates="child_messages"
    # )
    # child_messages: Mapped[List["ChatMessage"]] = relationship(
    #     "ChatMessage",
    #     remote_side=[parent_message_id],
    #     foreign_keys=[latest_child_message_id],
    #     back_populates="parent_message",
    # )


class ChatMessageRequest(BaseModel):
    # This is the primary-key (unique identifier) for the previous message of the tree
    alternate_agent_id: Optional[UUID] = Field(None, description="Alternate agent id")
    parent_message_id: Optional[UUID] = Field(None, description="Parent message id")
    latest_child_message_id: Optional[UUID] = Field(None, description="Latest child message id")
    message: str = Field(..., description="Message text")
    prompt_id: Optional[UUID] = Field(None, description="Prompt id")

    is_regenerated: bool = Field(False, description="Is regenerated message")


class ChatMessageResponse(BaseModel):
    id: str = Field(..., description="Chat message id")
    chat_session_id: str = Field(..., description="Chat session id")
    message: str = Field(..., description="Message text")
    message_type: MessageType = Field(..., description="Message type")
    parent_message_id: Optional[str] = Field(None, description="Parent message id")
    latest_child_message_id: Optional[str] = Field(None, description="Latest child message id")
    created_at: datetime = Field(..., description="Created at timestamp")
    updated_at: datetime = Field(..., description="Updated at timestamp")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ChatSessionRequest(BaseModel):
    agent_id: Optional[str] = Field(None, description="Agent id of the chat session")
    description: Optional[str] = Field(None, description="Description (Name) of the chat session")
    one_shot: bool = Field(False, description="One shot chat session")
    shared_status: ChatSessionSharedStatus = Field(ChatSessionSharedStatus.PRIVATE, description="Shared status")
    current_alternate_model: Optional[str] = Field(None, description="Current alternate model")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ChatSessionResponse(BaseModel):
    id: str = Field(..., description="Chat session id")
    description: Optional[str] = Field(None, description="Description (Name) of the chat session")
    agent_id: str = Field(..., description="Agent id of the chat session")
    agent_name: str = Field(..., description="Agent name of the chat session")
    messages: Optional[List[ChatMessageResponse]] = Field(None, description="Chat messages")
    created_at: datetime = Field(..., description="Created at timestamp")
    updated_at: datetime = Field(..., description="Updated at timestamp")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
