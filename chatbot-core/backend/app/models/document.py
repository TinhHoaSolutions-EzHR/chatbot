from datetime import datetime
from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from typing import List

from app.models import Base


class DocumentMetadata(Base):
    __tablename__ = "document_metadata"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    description = Column(String)
    object_url = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, default=None, nullable=True)

    tags = relationship(
        "DocumentMetadataTags",
        back_populates="document_metadata",
        cascade="all, delete-orphan",
    )


class DocumentMetadataTags(Base):
    __tablename__ = "document_metadata_tags"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    document_metadata_id = Column(Integer, ForeignKey("document_metadata.id"))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, default=None, nullable=True)

    document_metadata = relationship("DocumentMetadata", back_populates="tags")


class DocumentMetadataRequest(BaseModel):
    name: str = Field(..., description="Document name")
    description: str = Field(..., description="Document description")
    tags: List[str] = Field(default_factory=list, description="List of tags")

    class Config:
        from_attributes = True


class DocumentMetadataResponse(BaseModel):
    name: str = Field(..., description="Document name")
    description: str = Field(default="", description="Document description")
    tags: List[str] = Field(default_factory=list, description="List of tags")

    class Config:
        from_attributes = True
