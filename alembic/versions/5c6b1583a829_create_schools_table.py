"""create schools table

Revision ID: 5c6b1583a829
Revises: 24307d0babd4
Create Date: 2026-09-17 10:46:15.461456

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5c6b1583a829"
down_revision: Union[str, Sequence[str], None] = "24307d0babd4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create schools table."""

    op.create_table(
        "schools",

        # =====================================================
        # PRIMARY KEY
        # =====================================================

        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),

        # =====================================================
        # BASIC SCHOOL DETAILS
        # =====================================================

        sa.Column(
            "name",
            sa.String(length=255),
            nullable=False,
        ),

        sa.Column(
            "code",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "school_type",
            sa.String(length=50),
            nullable=True,
        ),

        sa.Column(
            "established_year",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "university_affiliation",
            sa.String(length=255),
            nullable=True,
        ),

        sa.Column(
            "accreditation",
            sa.String(length=255),
            nullable=True,
        ),

        # =====================================================
        # CONTACT INFORMATION
        # =====================================================

        sa.Column(
            "email",
            sa.String(length=255),
            nullable=False,
        ),

        sa.Column(
            "phone",
            sa.String(length=20),
            nullable=False,
        ),

        sa.Column(
            "website",
            sa.Text(),
            nullable=True,
        ),

        sa.Column(
            "principal_dean_name",
            sa.String(length=150),
            nullable=True,
        ),

        sa.Column(
            "contact_person",
            sa.String(length=150),
            nullable=True,
        ),

        # =====================================================
        # ADDRESS
        # =====================================================

        sa.Column(
            "address",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "city",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "state",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "country",
            sa.String(length=100),
            nullable=False,
            server_default="India",
        ),

        sa.Column(
            "pincode",
            sa.String(length=10),
            nullable=False,
        ),

        # =====================================================
        # ADDITIONAL INFORMATION
        # =====================================================

        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),

        sa.Column(
            "status",
            sa.String(length=30),
            nullable=False,
            server_default="active",
        ),

        # =====================================================
        # TIMESTAMPS
        # =====================================================

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        # =====================================================
        # CONSTRAINTS
        # =====================================================

        sa.PrimaryKeyConstraint("id"),

        sa.UniqueConstraint(
            "code",
            name="uq_schools_code",
        ),
    )

    # =========================================================
    # INDEXES
    # =========================================================

    op.create_index(
        "ix_schools_name",
        "schools",
        ["name"],
    )

    op.create_index(
        "ix_schools_code",
        "schools",
        ["code"],
    )

    op.create_index(
        "ix_schools_school_type",
        "schools",
        ["school_type"],
    )

    op.create_index(
        "ix_schools_email",
        "schools",
        ["email"],
    )

    op.create_index(
        "ix_schools_city",
        "schools",
        ["city"],
    )

    op.create_index(
        "ix_schools_state",
        "schools",
        ["state"],
    )

    op.create_index(
        "ix_schools_pincode",
        "schools",
        ["pincode"],
    )

    op.create_index(
        "ix_schools_status",
        "schools",
        ["status"],
    )


def downgrade() -> None:
    """Drop schools table."""

    op.drop_index(
        "ix_schools_status",
        table_name="schools",
    )

    op.drop_index(
        "ix_schools_pincode",
        table_name="schools",
    )

    op.drop_index(
        "ix_schools_state",
        table_name="schools",
    )

    op.drop_index(
        "ix_schools_city",
        table_name="schools",
    )

    op.drop_index(
        "ix_schools_email",
        table_name="schools",
    )

    op.drop_index(
        "ix_schools_school_type",
        table_name="schools",
    )

    op.drop_index(
        "ix_schools_code",
        table_name="schools",
    )

    op.drop_index(
        "ix_schools_name",
        table_name="schools",
    )

    op.drop_table("schools")