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
    from app.models import Prompt


class Agent(Base):
    """
    Represents an agent is a user that can interact with the chatbot.
    Tracks chat sessions and messages that the agent is involved in.
    """

    __tablename__ = "agent"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, index=True, default=uuid4
    )

    # Define relationships. We use the type hinting string to avoid circular imports.
    chat_sessions: Mapped[List["ChatSession"]] = relationship("ChatSession", back_populates="agent")
    chat_messages: Mapped[List["ChatMessage"]] = relationship("ChatMessage", back_populates="agent")
    prompt: Mapped["Prompt"] = relationship("Prompt", back_populates="agent")
