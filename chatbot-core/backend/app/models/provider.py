from datetime import datetime
from typing import List
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models import Base
from app.models.search import SearchSetting


class LLMProvider(Base):
    __tablename__ = "llm_providers"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String)
    provider: Mapped[str] = mapped_column(String)
    api_key: Mapped[str] = mapped_column(String)
    custom_config: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    default_model_name: Mapped[str] = mapped_column(String)
    fast_default_model_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    display_model_names: Mapped[List[str]] = mapped_column(String)
    is_default_provider: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)


class EmbeddingProvider(Base):
    __tablename__ = "embedding_providers"

    id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    api_key: Mapped[str] = mapped_column(String)
    provider_type: Mapped[LLMProvider] = mapped_column(SQLAlchemyEnum(LLMProvider, native_enum=False))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)

    search_settings: Mapped[List[SearchSetting]] = relationship("SearchSetting", back_populates="provider")
