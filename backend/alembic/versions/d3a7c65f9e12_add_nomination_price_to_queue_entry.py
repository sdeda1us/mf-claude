"""add nomination_price to queue_entry

Revision ID: d3a7c65f9e12
Revises: c8e1f4a92b7d
Create Date: 2026-09-08 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd3a7c65f9e12'
down_revision: Union[str, None] = 'c8e1f4a92b7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('queue_entries', sa.Column('nomination_price', sa.Numeric(10, 2), nullable=True))


def downgrade() -> None:
    op.drop_column('queue_entries', 'nomination_price')
