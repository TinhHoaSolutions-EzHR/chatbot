from datetime import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship
from uuid import uuid4

from app.models import Base


class Persona(Base):
    __tablename__ = "personas"

    id = Column(UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    deleted_at = Column(DateTime, default=None, nullable=True)

    chat_sessions = relationship("ChatSessions", back_populates="persona")
