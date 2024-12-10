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
# from app.models.user import User
# from app.models.relationship import AgentPrompt
# class Prompt(Base):
#     __tablename__ = "prompts"
#     id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
#         UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, index=True, default=uuid4
#     )
#     user_id: Mapped[UNIQUEIDENTIFIER] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
#     name: Mapped[str] = mapped_column(String)
#     description: Mapped[str] = mapped_column(String)
#     system_prompt: Mapped[str] = mapped_column(String)
#     task_prompt: Mapped[Optional[str]] = mapped_column(String, nullable=True)
#     include_citation: Mapped[bool] = mapped_column(Boolean, default=True)
#     is_datetime_aware: Mapped[bool] = mapped_column(Boolean, default=True)
#     is_default_prompt: Mapped[bool] = mapped_column(Boolean, default=False)
#     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
#     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
#     deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
#     user: Mapped["User"] = relationship("User", back_populates="prompts")
#     agents = relationship("Agent", secondary=AgentPrompt.__table__, back_populates="prompts")
