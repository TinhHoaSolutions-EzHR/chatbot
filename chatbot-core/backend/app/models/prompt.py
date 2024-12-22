from __future__ import annotations

from typing import List
from typing import Optional
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import ChatMessage
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
    agent_id: Mapped[UNIQUEIDENTIFIER] = mapped_column(ForeignKey("agent.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    task_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    include_citations: Mapped[bool] = mapped_column(Boolean, default=True)
    # Whether the prompt is datetime aware. If true, the prompt will be used to construct a datetime answer.
    datetime_aware: Mapped[bool] = mapped_column(Boolean, default=True)

    # Define relationships. We use the type hinting string to avoid circular imports.
    chat_messages: Mapped[List["ChatMessage"]] = relationship(
        "ChatMessage", back_populates="prompt"
    )
    agent: Mapped["Agent"] = relationship("Agent", back_populates="prompt")
