from __future__ import annotations

from datetime import datetime
from datetime import timezone
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
from sqlalchemy import NVARCHAR
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
    from app.models import Agent


class UserRole(str, Enum):
    """
    Enum for user roles.
    """

    ADMIN = "admin"
    BASIC = "basic"


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
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(NVARCHAR(None), nullable=True)
    avatar: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[UserRole] = mapped_column(
        SQLAlchemyEnum(UserRole, native_enum=False), nullable=False, default=UserRole.BASIC
    )
    is_oauth: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
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

    # Define relationships. We use the type hinting string to avoid circular imports.
    chat_sessions: Mapped[List["ChatSession"]] = relationship("ChatSession", back_populates="user")
    folders: Mapped[List["Folder"]] = relationship("Folder", back_populates="user")
    agents: Mapped[List["Agent"]] = relationship("Agent", back_populates="user")
    user_setting: Mapped["UserSetting"] = relationship("UserSetting", back_populates="user")


class UserSetting(Base):
    """
    Represents the user settings in the chatbot system.
    Tracks the settings for each user.
    """

    __tablename__ = "user_setting"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True, default=uuid4
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


class UserResponse(BaseModel):
    """
    Pydantic model for user response.
    Defines the fields that can be returned in the user.
    """

    id: UUID = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    name: str = Field(None, description="User name")
    avatar: Optional[str] = Field(None, description="User avatar")
    role: UserRole = Field(..., description="User role")
    created_at: datetime = Field(..., description="Created at")
    updated_at: datetime = Field(..., description="Updated at")

    class Config:
        from_attributes = True


class UserSettingsRequest(BaseModel):
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


class UserSettingsResponse(BaseModel):
    """
    Pydantic model for user settings response.
    Defines the fields that can be returned in the user settings.
    """

    recent_agent_ids: Optional[List[UUID]] = Field(
        default_factory=list, description="List of recent agent IDs"
    )
    auto_scroll: bool = Field(..., description="Auto scroll chat messages")
    default_model: Optional[str] = Field(None, description="Default model for the user")
    maximum_chat_retention_days: Optional[int] = Field(
        None, description="Maximum chat retention days"
    )

    class Config:
        from_attributes = True
