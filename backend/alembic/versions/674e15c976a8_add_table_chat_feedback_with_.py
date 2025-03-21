"""add table chat_feedback with relationship 1-1 table chat_message

Revision ID: 674e15c976a8
Revises: c2dc180ed8a7
Create Date: 2025-01-07 13:54:43.702832

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision: str = "674e15c976a8"
down_revision: Union[str, None] = "c2dc180ed8a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "chat_feedback",
        sa.Column("id", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("chat_message_id", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("is_positive", sa.Boolean(), nullable=False),
        sa.Column("feedback_text", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["chat_message_id"], ["chat_message.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("chat_feedback")
    # ### end Alembic commands ###
