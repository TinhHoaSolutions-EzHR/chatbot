from __future__ import annotations

from typing import List
from typing import Optional
from typing import TYPE_CHECKING
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from sqlalchemy import Boolean
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import ChatSession
    from app.models import Folder


class User(Base):
    """
    Represents a user in the chatbot system.
    Tracks all information related to the user.
    """

    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    recent_agent_ids: Mapped[str] = mapped_column(str, default_factory=str)
    auto_scroll: Mapped[bool] = mapped_column(Boolean, default=True)

    # Define relationships. We use the type hinting string to avoid circular imports.
    chat_sessions: Mapped[List["ChatSession"]] = relationship("ChatSession", back_populates="user")
    folders: Mapped[List["Folder"]] = relationship("Folder", back_populates="user")


class UserSettingRequest(BaseModel):
    """
    Pydantic model for user settings request.
    Defines the fields that can be updated in the user settings.
    """

    current_agent_id: Optional[UUID] = Field(None, title="Current using agent ID")
    auto_scroll: bool = Field(True, title="Auto scroll chat messages")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
