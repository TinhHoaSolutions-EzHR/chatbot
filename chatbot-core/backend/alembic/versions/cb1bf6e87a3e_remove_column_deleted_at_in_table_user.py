"""remove column deleted_at in table user

Revision ID: cb1bf6e87a3e
Revises: 3ddac298fb73
Create Date: 2025-01-07 17:07:22.428522

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision: str = "cb1bf6e87a3e"
down_revision: Union[str, None] = "3ddac298fb73"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "deleted_at")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user", sa.Column("deleted_at", mssql.DATETIMEOFFSET(), autoincrement=False, nullable=True)
    )
    # ### end Alembic commands ###