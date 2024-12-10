from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base import Base


# class AgentPrompt(Base):
#     __tablename__ = "agents__prompts"

#     agent_id: Mapped[UNIQUEIDENTIFIER] = mapped_column(ForeignKey("agents.id"), primary_key=True)
#     prompt_id: Mapped[UNIQUEIDENTIFIER] = mapped_column(ForeignKey("prompts.id"), primary_key=True)


class AgentTool(Base):
    __tablename__ = "agents__tools"

    agent_id: Mapped[UNIQUEIDENTIFIER] = mapped_column(ForeignKey("agents.id"), primary_key=True)
    tool_id: Mapped[UNIQUEIDENTIFIER] = mapped_column(ForeignKey("tools.id"), primary_key=True)
