"""add school to users

Revision ID: 80c243ff6037
Revises: fb6ec273c8c5
Create Date: 2026-09-18 12:55:25.284872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80c243ff6037'
down_revision: Union[str, Sequence[str], None] = 'fb6ec273c8c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add school_id to users table."""

    op.add_column(
        "users",
        sa.Column(
            "school_id",
            sa.UUID(),
            nullable=True,
        ),
    )

    op.create_foreign_key(
        "fk_users_school_id",
        "users",
        "schools",
        ["school_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.create_index(
        "ix_users_school_id",
        "users",
        ["school_id"],
    )


def downgrade() -> None:
    """Remove school_id from users table."""

    op.drop_index(
        "ix_users_school_id",
        table_name="users",
    )

    op.drop_constraint(
        "fk_users_school_id",
        "users",
        type_="foreignkey",
    )

    op.drop_column(
        "users",
        "school_id",
    )