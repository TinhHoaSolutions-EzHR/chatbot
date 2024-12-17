from datetime import datetime
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

from app.models.base import Base


class DocumentMetadata(Base):
    __tablename__ = "document_metadata"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    hidden: Mapped[bool] = mapped_column(Boolean, default=False)
    name: Mapped[str] = mapped_column(String)
    link: Mapped[str] = mapped_column(String)
    last_synced_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    primary_owners: Mapped[List[str]] = mapped_column(String)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    tags: Mapped[List["DocumentMetadataTag"]] = relationship("DocumentMetadataTag", back_populates="document_metadata")


class DocumentMetadataTag(Base):
    __tablename__ = "document_metadata_tag"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    tag_key: Mapped[str] = mapped_column(String)
    tag_value: Mapped[str] = mapped_column(String)
    document_metadata_id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        ForeignKey("document_metadata.id", ondelete="CASCADE")
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    document_metadata: Mapped[DocumentMetadata] = relationship("DocumentMetadata", back_populates="tags")


class DocumentUploadResponse(BaseModel):
    document_url: str = Field(..., description="Object URL")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
