from datetime import datetime
from datetime import timezone
from typing import List
from typing import Optional
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


class Document(Base):
    """
    Represents a document that contains information about uploaded documents.
    Tracks and organizes uploaded documents.
    """

    __tablename__ = "document"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    last_synced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    issue_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    is_outdated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
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

    tags: Mapped[List["DocumentTag"]] = relationship("DocumentTag", back_populates="document")


class DocumentTag(Base):
    """
    Represents a document tag that contains information about uploaded documents's tags.
    Tracks and organizes uploaded documents's tags.
    """

    __tablename__ = "document_tag"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid4
    )
    tag_key: Mapped[str] = mapped_column(String, nullable=False)
    tag_value: Mapped[str] = mapped_column(String, nullable=False)
    document_id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        ForeignKey("document.id", ondelete="CASCADE")
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

    # Define relationships.``
    document: Mapped["Document"] = relationship("Document", back_populates="tags")


class DocumentResponse(BaseModel):
    """
    Pydantic model for document upload response.
    Defines the structure of document upload returned to the client.
    """

    document_url: str = Field(..., description="Object URL")

    class Config:
        from_attributes = True
