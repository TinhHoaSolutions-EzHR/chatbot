"""add foreign from document_metadata to document_metadata_tag

Revision ID: 46fc46c959c4
Revises: 92a9ffaf27e3
Create Date: 2025-01-07 13:34:16.832273

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision: str = "46fc46c959c4"
down_revision: Union[str, None] = "92a9ffaf27e3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "document_metadata_tag",
        sa.Column("document_metadata_id", mssql.UNIQUEIDENTIFIER(), nullable=False),
    )
    op.create_foreign_key(
        None,
        "document_metadata_tag",
        "document_metadata",
        ["document_metadata_id"],
        ["id"],
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "document_metadata_tag", type_="foreignkey")
    op.drop_column("document_metadata_tag", "document_metadata_id")
    # ### end Alembic commands ###