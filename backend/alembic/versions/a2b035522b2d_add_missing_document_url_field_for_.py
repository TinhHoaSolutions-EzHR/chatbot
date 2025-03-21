"""add missing document_url field for document metadata table

Revision ID: a2b035522b2d
Revises: a51a76136ba9
Create Date: 2025-01-15 10:40:40.495858

"""

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "a2b035522b2d"
down_revision: Union[str, None] = "a51a76136ba9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("document_metadata", sa.Column("document_url", sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("document_metadata", "document_url")
    # ### end Alembic commands ###
