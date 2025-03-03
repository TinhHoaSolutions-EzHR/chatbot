"""add table embedding_provider

Revision ID: 0e8338e6a569
Revises: 46fc46c959c4
Create Date: 2025-01-07 13:37:56.228265

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision: str = "0e8338e6a569"
down_revision: Union[str, None] = "46fc46c959c4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "embedding_provider",
        sa.Column("dimensions", sa.Integer(), nullable=False),
        sa.Column("embed_batch_size", sa.Integer(), nullable=False),
        sa.Column("id", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column(
            "name",
            sa.Enum("OPENAI", "GEMINI", "COHERE", name="providertype", native_enum=False),
            nullable=False,
        ),
        sa.Column("api_key", sa.LargeBinary(), nullable=True),
        sa.Column("models", sa.String(), nullable=True),
        sa.Column("current_model", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_default_provider", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("embedding_provider")
    # ### end Alembic commands ###
