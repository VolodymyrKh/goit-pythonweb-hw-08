"""create contacts table

Revision ID: 0001
Revises:
Create Date: 2026-09-24 21:10:00

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "contacts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=50), nullable=False),
        sa.Column("last_name", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=False),
        sa.Column("birthday", sa.Date(), nullable=False),
        sa.Column("additional_data", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(
        op.f("ix_contacts_first_name"), "contacts", ["first_name"], unique=False
    )
    op.create_index(
        op.f("ix_contacts_last_name"), "contacts", ["last_name"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_contacts_last_name"), table_name="contacts")
    op.drop_index(op.f("ix_contacts_first_name"), table_name="contacts")
    op.drop_table("contacts")
