from __future__ import annotations

from typing import List
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import ChatSession
    from app.models import ChatMessage


class User(Base):
    """
    Represents a user in the chatbot system.
    Tracks all information related to the user.
    """

    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, index=True, default=uuid4
    )

    chat_sessions: Mapped[List["ChatSession"]] = relationship("ChatSession", back_populates="user")
    chat_messages: Mapped[List["ChatMessage"]] = relationship("ChatMessage", back_populates="user")
