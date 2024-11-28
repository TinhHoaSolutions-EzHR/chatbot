from datetime import datetime
from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4

from app.models import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    persona_id = Column(UUID(as_uuid=True), nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, default=None, nullable=True)

    user = relationship("User", back_populates="chat_sessions")
    persona = relationship("Persona", back_populates="chat_sessions")
    chat_messages = relationship(
        "ChatMessages", back_populates="chat_session", cascade="all, delete-orphan"
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    chat_session_id = Column(UUID(as_uuid=True), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, default=None, nullable=True)

    chat_session = relationship("ChatSessions", back_populates="chat_messages")


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
    created_at: datetime = Field(..., description="Created at timestamp")
    updated_at: datetime = Field(..., description="Updated at timestamp")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ChatMessageRequest(BaseModel):
    # This is the primary-key (unique identifier) for the previous message of the tree
    parent_message_id: int | None = Field(None, description="Parent message id")
    message: str = Field(..., description="Message text")
