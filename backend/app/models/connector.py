from datetime import datetime
from datetime import timezone
from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field
from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import func
from sqlalchemy import String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base import Base


class DocumentSource(str, Enum):
    """
    Enumeration of document sources.
    """

    FILE = "file"
    GOOGLE_DRIVE = "google_drive"


class Connector(Base):
    """
    Represents a connector that contains information about uploaded documents.
    Tracks and organizes the connector for uploaded documents.
    """

    __tablename__ = "connector"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[DocumentSource] = mapped_column(
        SQLAlchemyEnum(DocumentSource, native_enum=False),
        nullable=False,
        default=DocumentSource.FILE,
    )
    connector_specific_config: Mapped[str] = mapped_column(String, nullable=True)
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


class ConnectorRequest(BaseModel):
    """
    Pydantic model for connector request.
    Defines the structure of connector data received from the client.
    """

    name: Optional[str] = Field(None, description="Connector name")
    file_paths: List[str] = Field(default_factory=list, description="List of uploaded file paths")

    class Config:
        from_attributes = True


class ConnectorResponse(BaseModel):
    """
    Pydantic model for connector response.
    Defines the structure of connector data returned to the client.
    """

    id: UUID = Field(..., description="Connector ID")
    name: str = Field(..., description="Connector name")
    source: DocumentSource = Field(..., description="Document source")
    connector_specific_config: Optional[Dict[str, Any]] = Field(
        None, description="Connector specific configuration"
    )
    created_at: datetime = Field(..., description="Created at timestamp")
    updated_at: datetime = Field(..., description="Updated at timestamp")
    deleted_at: Optional[datetime] = Field(None, description="Deleted at timestamp")

    class Config:
        from_attributes = True
