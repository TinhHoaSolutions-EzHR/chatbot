from __future__ import annotations

from datetime import datetime
from datetime import timezone
from typing import List
from typing import Optional
from typing import TYPE_CHECKING
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

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
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )

    # Define relationships. We use the type hinting string to avoid circular imports.
    chat_sessions: Mapped[List["ChatSession"]] = relationship("ChatSession", back_populates="user")
    folders: Mapped[List["Folder"]] = relationship("Folder", back_populates="user")
    user_setting: Mapped["UserSetting"] = relationship("UserSetting", back_populates="user")


class UserSetting(Base):
    """
    Represents the user settings in the chatbot system.
    Tracks the settings for each user.
    """

    __tablename__ = "user_setting"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    recent_agent_ids: Mapped[str] = mapped_column(String, default="")
    auto_scroll: Mapped[bool] = mapped_column(Boolean, default=True)
    default_model: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )

    # Define relationships.
    user: Mapped["User"] = relationship("User", back_populates="user_setting")


class UserSettingRequest(BaseModel):
    """
    Pydantic model for user settings request.
    Defines the fields that can be updated in the user settings.
    """

    current_agent_id: Optional[UUID] = Field(None, description="Current using agent ID")
    auto_scroll: bool = Field(True, description="Auto scroll chat messages")
    default_model: Optional[str] = Field(None, description="Default model for the user")
    maximum_chat_retention_days: Optional[int] = Field(
        None, description="Maximum chat retention days"
    )

    class Config:
        from_attributes = True


class UserSettingResponse(BaseModel):
    """
    Pydantic model for user settings response.
    Defines the fields that can be returned in the user settings.
    """

    recent_agent_ids: Optional[List[UUID]] = Field(None, description="List of recent agent IDs")
    auto_scroll: bool = Field(..., description="Auto scroll chat messages")
    default_model: Optional[str] = Field(None, description="Default model for the user")
    maximum_chat_retention_days: Optional[int] = Field(
        None, description="Maximum chat retention days"
    )

    class Config:
        from_attributes = True
