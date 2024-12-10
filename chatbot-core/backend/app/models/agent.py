from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List
from typing import Optional
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing_extensions import TypedDict

from app.models.base import Base
from app.models.relationship import AgentTool
from app.models.tool import Tool
# from app.models.prompt import Prompt
# from app.models.relationship import AgentPrompt

if TYPE_CHECKING:
    from app.models import ChatSession
    from app.models import ChatMessage


class StarterMessages(TypedDict):
    name: str
    message: str


class RecencyBiasSetting(str, Enum):
    FAVOR_RECENT = "favor_recent"
    BASE_DECAY = "base_decay"
    NO_DECAY = "no_decay"
    AUTO = "auto"


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    description: Mapped[str] = mapped_column(String(255))
    num_chunks: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    chunks_above: Mapped[int] = mapped_column(Integer)
    chunks_below: Mapped[int] = mapped_column(Integer)
    llm_relevance_filter: Mapped[bool] = mapped_column(Boolean)
    llm_filter_extraction: Mapped[bool] = mapped_column(Boolean)
    recency_bias: Mapped[RecencyBiasSetting] = mapped_column(SQLAlchemyEnum(RecencyBiasSetting, native_enum=False))
    starter_messages: Mapped[Optional[List[StarterMessages]]] = mapped_column(String, nullable=True)
    is_visible: Mapped[bool] = mapped_column(Boolean)
    display_priority: Mapped[int] = mapped_column(Integer)
    uploaded_image_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    icon_color: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    icon_shaped: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    # Use string-based relationship to break circular import
    # prompts: Mapped[List[Prompt]] = relationship("Prompt", secondary=AgentPrompt.__table__, back_populates="agents")
    chat_sessions: Mapped[List[ChatSession]] = relationship("ChatSession", back_populates="agent")
    chat_messages: Mapped[List[ChatMessage]] = relationship("ChatMessage", back_populates="agent")
    tools: Mapped[List[Tool]] = relationship("Tool", secondary=AgentTool.__table__, back_populates="agents")
