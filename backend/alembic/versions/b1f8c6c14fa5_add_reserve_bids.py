"""add reserve bids

Revision ID: b1f8c6c14fa5
Revises: d7485a6e8ff0
Create Date: 2026-08-13 16:24:22.077104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'b1f8c6c14fa5'
down_revision: Union[str, None] = 'd7485a6e8ff0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('reserve_bids',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('auction_item_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('max_amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['auction_item_id'], ['auction_items.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('auction_item_id', 'user_id', name='uq_reserve_item_user')
    )


def downgrade() -> None:
    op.drop_table('reserve_bids')
