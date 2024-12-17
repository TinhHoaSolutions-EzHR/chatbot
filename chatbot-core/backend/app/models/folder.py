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
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base

if TYPE_CHECKING:
    from app.models import User
    from app.models import ChatSession


class Folder(Base):
    """
    Represents a folder that contains chat sessions.
    Tracks and organizes chat sessions that are stored in the folder.
    """

    __tablename__ = "folders"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UNIQUEIDENTIFIER] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(str, nullable=True)
    display_priority: Mapped[Optional[int]] = mapped_column(int, nullable=True, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=lambda: datetime.now(timezone.utc)
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    # Define relationships
    user: Mapped["User"] = relationship("User", back_populates="chat_sessions", cascade="save-update, merge")
    chat_sessions: Mapped[List["ChatSession"]] = relationship("ChatSession", back_populates="folder")

    def __lt__(self, other: Folder) -> bool:
        if not isinstance(other, Folder):
            return NotImplemented

        if self.display_priority == other.display_priority:
            # Bigger ID (created later) show earlier
            return self.id > other.id

        return self.display_priority < other.display_priority


class FolderRequest(BaseModel):
    """
    Pydantic model for folder request.
    Defines the structure of folder data received from the client.
    """

    name: Optional[str] = Field(None, description="Folder name")


class FolderResponse(BaseModel):
    """
    Pydantic model for folder response.
    Defines the structure of folder data returned to the client.
    """

    id: UUID = Field(..., description="Folder ID")
    user_id: UUID = Field(..., description="User ID")
    name: Optional[str] = Field(None, description="Folder name")
    display_priority: Optional[int] = Field(0, description="Folder display priority")
    chat_sessions: List[ChatSession] = Field([], description="Chat sessions in the folder")
