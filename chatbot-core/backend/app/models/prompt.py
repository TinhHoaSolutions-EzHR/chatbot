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
    from app.models.chat import ChatMessage


class Prompt(Base):
    """
    Represents a prompt in the chatbot system.
    Tracks answer is being constructed for the prompt.
    """

    __tablename__ = "prompt"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid4)

    # Define relationships. We use the type hinting string to avoid circular imports.
    chat_messages: Mapped[List["ChatMessage"]] = relationship("ChatMessage", back_populates="prompt")
