"""add auto_pass_if_exceeded to reserve_bid

Revision ID: f7c3b6a1e8d5
Revises: e2a4f8c1d9b3
Create Date: 2026-09-16 09:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f7c3b6a1e8d5'
down_revision: Union[str, None] = 'e2a4f8c1d9b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'reserve_bids',
        sa.Column('auto_pass_if_exceeded', sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    op.drop_column('reserve_bids', 'auto_pass_if_exceeded')
