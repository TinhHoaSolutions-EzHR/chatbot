from datetime import datetime
from enum import Enum
from typing import List
from typing import Optional
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base import Base


class DocumentSource(str, Enum):
    FILE = "file"
    GOOGLE_DRIVE = "google_drive"


class Connector(Base):
    __tablename__ = "connectors"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[DocumentSource] = mapped_column(SQLAlchemyEnum(DocumentSource, native_enum=False), nullable=False)
    connector_specific_config: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)


class ConnectorRequest(BaseModel):
    name: str = Field(..., description="Connector name")
    file_paths: List[str] = Field(default_factory=list, description="List of uploaded file paths")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ConnectorResponse(BaseModel):
    id: UUID = Field(..., description="Connector ID")
    name: str = Field(..., description="Connector name")
    source: DocumentSource = Field(..., description="Document source")
    connector_specific_config: Optional[str] = Field(None, description="Connector specific configuration")
    created_at: datetime = Field(..., description="Created at timestamp")
    updated_at: datetime = Field(..., description="Updated at timestamp")
    deleted_at: Optional[datetime] = Field(None, description="Deleted at timestamp")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
