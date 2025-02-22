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
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base
from app.models.chat import ChatSessionResponse

if TYPE_CHECKING:
    from app.models import User
    from app.models import ChatSession


class Folder(Base):
    """
    Represents a folder that contains chat sessions.
    Tracks and organizes chat sessions that are stored in the folder.
    """

    __tablename__ = "folder"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid4
    )
    user_id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
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

    # Define relationships
    user: Mapped["User"] = relationship("User", back_populates="folders")
    chat_sessions: Mapped[List["ChatSession"]] = relationship(
        "ChatSession", back_populates="folder"
    )


class FolderRequest(BaseModel):
    """
    Pydantic model for folder request.
    Defines the structure of folder data received from the client.
    """

    name: Optional[str] = Field(None, description="Folder name")

    class Config:
        from_attributes = True


class FolderResponse(BaseModel):
    """
    Pydantic model for folder response.
    Defines the structure of folder data returned to the client.
    """

    id: UUID = Field(..., description="Folder ID")
    user_id: UUID = Field(..., description="User ID")
    name: Optional[str] = Field(None, description="Folder name")
    chat_sessions: List[ChatSessionResponse] = Field([], description="Chat sessions in the folder")

    class Config:
        from_attributes = True
