"""add reserve_price to queue_entry

Revision ID: c8e1f4a92b7d
Revises: f3b9c1a7d2e4
Create Date: 2026-09-07 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c8e1f4a92b7d'
down_revision: Union[str, None] = 'f3b9c1a7d2e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('queue_entries', sa.Column('reserve_price', sa.Numeric(10, 2), nullable=True))


def downgrade() -> None:
    op.drop_column('queue_entries', 'reserve_price')
