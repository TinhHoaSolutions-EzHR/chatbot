from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Integer, String, JSON
from typing import Optional, List, Dict

from app.models import Base


class DocumentSource(str, Enum):
    FILE = "file"
    GOOGLE_DRIVE = "google_drive"


class Connector(Base):
    __tablename__ = "connectors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    source = Column(String)
    connector_specific_config = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, default=None, nullable=True)


class ConnectorRequest(BaseModel):
    name: str = Field(..., description="Connector name")
    file_paths: List[str] = Field(default_factory=list, description="List of uploaded file paths")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class ConnectorResponse(BaseModel):
    id: int = Field(..., description="Connector ID")
    name: str = Field(..., description="Connector name")
    source: DocumentSource = Field(..., description="Document source")
    connector_specific_config: Optional[Dict] = Field(..., description="Connector specific configuration")
    created_at: datetime = Field(..., description="Created at timestamp")
    updated_at: datetime = Field(..., description="Updated at timestamp")
    deleted_at: Optional[datetime] = Field(..., description="Deleted at timestamp")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
