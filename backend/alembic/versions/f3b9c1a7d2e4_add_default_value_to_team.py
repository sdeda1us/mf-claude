"""add default_value to team

Revision ID: f3b9c1a7d2e4
Revises: a294bf258e5b
Create Date: 2026-08-21 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f3b9c1a7d2e4'
down_revision: Union[str, None] = 'a294bf258e5b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('teams', sa.Column('default_value', sa.Numeric(10, 2), nullable=True))


def downgrade() -> None:
    op.drop_column('teams', 'default_value')
