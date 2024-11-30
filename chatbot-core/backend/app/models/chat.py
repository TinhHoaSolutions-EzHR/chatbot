from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, String, Text, ForeignKey, func
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER as UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List
from uuid import uuid4

from app.models import Base
from app.models.user import User
from app.models.persona import Persona


class MessageType(str, Enum):
    SYSTEM = "system"  # SystemMessage
    USER = "user"  # HumanMessage
    ASSISTANT = "assistant"  # AIMessage


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    persona_id: Mapped[UUID] = mapped_column(ForeignKey("personas.id"), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    user: Mapped[User] = relationship("User", back_populates="chat_sessions")
    persona: Mapped[Persona] = relationship("Persona", back_populates="chat_sessions")
    chat_messages: Mapped[List["ChatMessage"]] = relationship(
        "ChatMessage", back_populates="chat_sessions", lazy="selectin"
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    chat_session_id: Mapped[UUID] = mapped_column(ForeignKey("chat_sessions.id"), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    message_type: Mapped[MessageType] = mapped_column(SQLAlchemyEnum(MessageType, native_enum=False), nullable=False)
    parent_message_id: Mapped[UUID] = mapped_column(ForeignKey("chat_messages.id"), nullable=True)
    latest_child_message_id: Mapped[UUID] = mapped_column(ForeignKey("chat_messages.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    chat_session: Mapped[ChatSession] = relationship("ChatSession", back_populates="chat_messages")
    parent_message: Mapped["ChatMessage"] = relationship("ChatMessage", remote_side=[id], back_populates="replies")
    replies: Mapped[List["ChatMessage"]] = relationship("ChatMessage", back_populates="parent_message")


class ChatMessageRequest(BaseModel):
    # This is the primary-key (unique identifier) for the previous message of the tree
    message: str = Field(..., description="Message text", default=None)
    latest_child_message_id: str | None = Field(None, description="Latest child message id", default=None)


class ChatMessageResponse(BaseModel):
    id: str = Field(..., description="Chat message id")
    chat_session_id: str = Field(..., description="Chat session id")
    message: str = Field(..., description="Message text")
    message_type: MessageType = Field(..., description="Message type")
    parent_message_id: str | None = Field(None, description="Parent message id")
    created_at: datetime = Field(..., description="Created at timestamp")
    updated_at: datetime = Field(..., description="Updated at timestamp")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ChatSessionRequest(BaseModel):
    persona_id: str = Field(..., description="Persona id of the chat session")
    description: str = Field(..., description="Description (Name) of the chat session")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ChatSessionResponse(BaseModel):
    id: str = Field(..., description="Chat session id")
    description: str = Field(..., description="Description (Name) of the chat session")
    persona_id: str = Field(..., description="Persona id of the chat session")
    persona_name: str = Field(..., description="Persona name of the chat session")
    messages: List[ChatMessageResponse] | None = Field(..., description="Chat messages", default=None)
    created_at: datetime = Field(..., description="Created at timestamp")
    updated_at: datetime = Field(..., description="Updated at timestamp")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
