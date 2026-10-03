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
    # batch_alter_table so this also works on SQLite, which can't ALTER in
    # a foreign key outside of batch mode (recreate-table) -- plain
    # op.create_foreign_key here fails with NotImplementedError on SQLite.
    # Equivalent to the original two bare calls on Postgres/other dialects.
    with op.batch_alter_table('auction_items') as batch_op:
        batch_op.add_column(sa.Column('nominated_by_user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_auction_items_nominated_by_user_id',
            'users',
            ['nominated_by_user_id'], ['id'],
        )


def downgrade() -> None:
    with op.batch_alter_table('auction_items') as batch_op:
        batch_op.drop_constraint('fk_auction_items_nominated_by_user_id', type_='foreignkey')
        batch_op.drop_column('nominated_by_user_id')
