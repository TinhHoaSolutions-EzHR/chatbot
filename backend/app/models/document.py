from datetime import datetime
from datetime import timezone
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import NVARCHAR
from sqlalchemy import String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

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
    name: Mapped[str] = mapped_column(NVARCHAR(255), nullable=False)
    last_synced_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    document_url: Mapped[str] = mapped_column(String, nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
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


class DocumentUploadResponse(BaseModel):
    """
    Pydantic model for document upload response.
    Defines the structure of document upload returned to the client.
    """

    task_id: str = Field(..., description="Indexing background task ID")
    document_url: str = Field(..., description="Uploaded document url")

    class Config:
        from_attributes = True
