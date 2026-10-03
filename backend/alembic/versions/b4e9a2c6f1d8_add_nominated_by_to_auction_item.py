"""add nominated_by_user_id to auction_item

Revision ID: b4e9a2c6f1d8
Revises: f7c3b6a1e8d5
Create Date: 2026-10-03 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b4e9a2c6f1d8'
down_revision: Union[str, None] = 'f7c3b6a1e8d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'auction_items', sa.Column('nominated_by_user_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        'fk_auction_items_nominated_by_user_id',
        'auction_items', 'users',
        ['nominated_by_user_id'], ['id'],
    )


def downgrade() -> None:
    op.drop_constraint('fk_auction_items_nominated_by_user_id', 'auction_items', type_='foreignkey')
    op.drop_column('auction_items', 'nominated_by_user_id')
