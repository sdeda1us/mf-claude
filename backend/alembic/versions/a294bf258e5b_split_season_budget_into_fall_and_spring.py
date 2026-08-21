"""split season budget into fall and spring

Revision ID: a294bf258e5b
Revises: b1f8c6c14fa5
Create Date: 2026-08-20 21:52:59.809236

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a294bf258e5b'
down_revision: Union[str, None] = 'b1f8c6c14fa5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "seasons",
        sa.Column("fall_budget_per_user", sa.Numeric(10, 2), nullable=False, server_default="400"),
    )
    op.add_column(
        "seasons",
        sa.Column("spring_budget_per_user", sa.Numeric(10, 2), nullable=False, server_default="240"),
    )
    op.drop_column("seasons", "budget_per_user")


def downgrade() -> None:
    op.add_column(
        "seasons",
        sa.Column("budget_per_user", sa.Numeric(10, 2), nullable=False, server_default="600"),
    )
    op.drop_column("seasons", "fall_budget_per_user")
    op.drop_column("seasons", "spring_budget_per_user")
