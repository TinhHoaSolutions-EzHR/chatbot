# from datetime import datetime
# from typing import Optional
# from uuid import uuid4
# from sqlalchemy import Boolean
# from sqlalchemy import DateTime
# from sqlalchemy import ForeignKey
# from sqlalchemy import String
# from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship
# from app.models.base import Base
# class SearchSetting(Base):
#     __tablename__ = "search_settings"
#     id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
#         UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, index=True, default=uuid4
#     )
#     model_name: Mapped[str] = mapped_column(String)
#     model_dim: Mapped[int] = mapped_column(int)
#     normalize: Mapped[bool] = mapped_column(Boolean)
#     query_prefix: Mapped[Optional[str]] = mapped_column(String, nullable=True)
#     passage_prefix: Mapped[Optional[str]] = mapped_column(String, nullable=True)
#     index_name: Mapped[str] = mapped_column(String)
#     status: Mapped[str] = mapped_column(String)
#     provider_type: Mapped[Optional[str]] = mapped_column(
#         ForeignKey("llm_providers.id", ondelete="CASCADE"), nullable=True
#     )
#     # multipass_indexing: Mapped[bool] = mapped_column(Boolean, default=True)
#     # multilingual_expansion: Mapped[List[str]] = mapped_column(
#     #     String, default=[]
#     # )
#     # disable_rerank_for_streaming: Mapped[bool] = mapped_column(Boolean, default=False)
#     # rerank_model_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
#     # rerank_provider_type: Mapped[RerankerProvider | None] = mapped_column(
#     #     Enum(RerankerProvider, native_enum=False), nullable=True
#     # )
#     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
#     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
#     deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
#     # provider: Mapped[LLMProvider] = relationship("LLMProvider", back_populates="search_settings")
# class SearchDoc(Base):
#     __tablename__ = "search_docs"
#     id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
#         UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, index=True, default=uuid4
#     )
