# from datetime import datetime
# from typing import Optional
# from uuid import uuid4
# from sqlalchemy import Boolean
# from sqlalchemy import DateTime
# from sqlalchemy import Float
# from sqlalchemy import Integer
# from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
# from app.models.base import Base
# class TokenRateLimit(Base):
#     __tablename__ = "token_rate_limits"
#     id: Mapped[UNIQUEIDENTIFIER] = mapped_column(
#         UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, index=True, default=uuid4
#     )
#     is_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
#     token_budget: Mapped[int] = mapped_column(Integer, default=1000)
#     period_hours: Mapped[float] = mapped_column(Float, default=24.0)
#     created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now)
#     updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
#     deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
