"""add home_score/away_score to scheduled_games

Revision ID: a1b2c3d4e5f6
Revises: c4f8a2e6b9d1
Create Date: 2026-10-07 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = 'c4f8a2e6b9d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('scheduled_games', sa.Column('home_score', sa.Integer(), nullable=True))
    op.add_column('scheduled_games', sa.Column('away_score', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('scheduled_games', 'away_score')
    op.drop_column('scheduled_games', 'home_score')
