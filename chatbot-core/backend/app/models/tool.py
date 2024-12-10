from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List
from typing import Optional
from uuid import uuid4

from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing_extensions import TypedDict

from app.models.base import Base
from app.models.relationship import AgentTool


class ToolType(str, Enum):
    FUNCTION = "function"
    QUERY_ENGINE = "query_engine"


class HeaderItemDict(TypedDict):
    key: str
    value: str


class Tool(Base):
    __tablename__ = "tools"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    display_name: Mapped[str] = mapped_column(String)
    tool_type: Mapped[ToolType] = mapped_column(SQLAlchemyEnum(ToolType, native_enum=False))
    custom_headers: Mapped[Optional[List[HeaderItemDict]]] = mapped_column(String, nullable=True)
    openapi_schema: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    agents: Mapped[List] = relationship("Agent", secondary=AgentTool.__table__, back_populates="tools")
