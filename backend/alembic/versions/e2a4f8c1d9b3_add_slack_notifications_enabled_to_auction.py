"""add slack_notifications_enabled to auction

Revision ID: e2a4f8c1d9b3
Revises: d3a7c65f9e12
Create Date: 2026-09-15 09:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e2a4f8c1d9b3'
down_revision: Union[str, None] = 'd3a7c65f9e12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'auctions',
        sa.Column('slack_notifications_enabled', sa.Boolean(), nullable=False, server_default=sa.true()),
    )


def downgrade() -> None:
    op.drop_column('auctions', 'slack_notifications_enabled')
