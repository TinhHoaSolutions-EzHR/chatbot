"""remove agent_id from table chat_message

Revision ID: a51a76136ba9
Revises: 989953ae75e5
Create Date: 2025-01-10 11:45:44.423472

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision: str = "a51a76136ba9"
down_revision: Union[str, None] = "989953ae75e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("FK_chat_message__agent", "chat_message", type_="foreignkey")
    op.drop_column("chat_message", "agent_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "chat_message",
        sa.Column("agent_id", mssql.UNIQUEIDENTIFIER(), autoincrement=False, nullable=False),
    )
    op.create_foreign_key("FK_chat_message__agent", "chat_message", "agent", ["agent_id"], ["id"])
    # ### end Alembic commands ###
