"""add team_daily_scores

Revision ID: 970a4317ccf7
Revises: b4e9a2c6f1d8
Create Date: 2026-10-03 11:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '970a4317ccf7'
down_revision: Union[str, None] = 'b4e9a2c6f1d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'team_daily_scores',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('team_id', sa.Integer(), nullable=False),
        sa.Column('league', sa.String(length=50), nullable=False),
        sa.Column('season_label', sa.String(length=20), nullable=False),
        sa.Column('as_of_date', sa.Date(), nullable=False),
        sa.Column('stats', sa.JSON(), nullable=False),
        sa.Column('score', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('team_id', 'season_label', 'as_of_date', name='uq_team_daily_score'),
    )


def downgrade() -> None:
    op.drop_table('team_daily_scores')
