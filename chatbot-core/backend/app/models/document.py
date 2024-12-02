from datetime import datetime
from pydantic import BaseModel, Field
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import List, Optional
from uuid import uuid4

from app.models import Base


class DocumentMetadata(Base):
    __tablename__ = "document_metadata"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    document_url: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    tags: Mapped[List["DocumentMetadataTags"]] = relationship(
        "DocumentMetadataTags", back_populates="document_metadata", lazy="joined"
    )


class DocumentMetadataTags(Base):
    __tablename__ = "document_metadata_tags"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    document_metadata_id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), ForeignKey("document_metadata.id"), nullable=False
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
