"""add user

Revision ID: ff513f9e349f
Revises: b8a619f44d93
Create Date: 2024-12-29 08:07:25.071301

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision: str = "ff513f9e349f"
down_revision: Union[str, None] = "b8a619f44d93"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user_setting",
        sa.Column("id", mssql.UNIQUEIDENTIFIER(), nullable=False),
        sa.Column("recent_agent_ids", sa.String(), nullable=False),
        sa.Column("auto_scroll", sa.Boolean(), nullable=False),
        sa.Column("default_model", sa.String(), nullable=True),
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
        sa.ForeignKeyConstraint(["id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
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
    op.add_column("agent", sa.Column("user_id", mssql.UNIQUEIDENTIFIER(), nullable=True))
    op.add_column("agent", sa.Column("prompt_id", mssql.UNIQUEIDENTIFIER(), nullable=False))
    op.add_column("agent", sa.Column("name", sa.String(), nullable=False))
    op.add_column("agent", sa.Column("description", sa.String(), nullable=True))
    op.add_column(
        "agent",
        sa.Column(
            "agent_type",
            sa.Enum("SYSTEM", "USER", name="agenttype", native_enum=False),
            nullable=False,
        ),
    )
    op.add_column("agent", sa.Column("is_visible", sa.Boolean(), nullable=False))
    op.add_column("agent", sa.Column("display_priority", sa.String(), nullable=False))
    op.add_column("agent", sa.Column("uploaded_image_path", sa.String(), nullable=True))
    op.add_column(
        "agent",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )
    op.add_column(
        "agent",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )
    op.add_column("agent", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    op.create_foreign_key(None, "agent", "user", ["user_id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key(None, "agent", "prompt", ["prompt_id"], ["id"])
    op.drop_constraint("FK__chat_mess__promp__3E52440B", "chat_message", type_="foreignkey")
    op.drop_column("chat_message", "prompt_id")
    op.add_column(
        "prompt",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )
    op.add_column(
        "prompt",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )
    op.add_column("prompt", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    op.drop_constraint("FK__prompt__agent_id__2F10007B", "prompt", type_="foreignkey")
    op.drop_column("prompt", "include_citations")
    op.drop_column("prompt", "datetime_aware")
    op.drop_column("prompt", "agent_id")
    op.add_column(
        "user",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )
    op.add_column(
        "user",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )
    op.add_column("user", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    op.drop_index("ix_user_id", table_name="user")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index("ix_user_id", "user", ["id"], unique=False)
    op.drop_column("user", "deleted_at")
    op.drop_column("user", "updated_at")
    op.drop_column("user", "created_at")
    op.add_column(
        "prompt",
        sa.Column("agent_id", mssql.UNIQUEIDENTIFIER(), autoincrement=False, nullable=False),
    )
    op.add_column(
        "prompt", sa.Column("datetime_aware", mssql.BIT(), autoincrement=False, nullable=False)
    )
    op.add_column(
        "prompt", sa.Column("include_citations", mssql.BIT(), autoincrement=False, nullable=False)
    )
    op.create_foreign_key("FK__prompt__agent_id__2F10007B", "prompt", "agent", ["agent_id"], ["id"])
    op.drop_column("prompt", "deleted_at")
    op.drop_column("prompt", "updated_at")
    op.drop_column("prompt", "created_at")
    op.add_column(
        "chat_message",
        sa.Column("prompt_id", mssql.UNIQUEIDENTIFIER(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "FK__chat_mess__promp__3E52440B", "chat_message", "prompt", ["prompt_id"], ["id"]
    )
    op.drop_constraint(None, "agent", type_="foreignkey")
    op.drop_constraint(None, "agent", type_="foreignkey")
    op.drop_column("agent", "deleted_at")
    op.drop_column("agent", "updated_at")
    op.drop_column("agent", "created_at")
    op.drop_column("agent", "uploaded_image_path")
    op.drop_column("agent", "display_priority")
    op.drop_column("agent", "is_visible")
    op.drop_column("agent", "agent_type")
    op.drop_column("agent", "description")
    op.drop_column("agent", "name")
    op.drop_column("agent", "prompt_id")
    op.drop_column("agent", "user_id")
    op.drop_table("chat_feedback")
    op.drop_table("user_setting")
    # ### end Alembic commands ###
