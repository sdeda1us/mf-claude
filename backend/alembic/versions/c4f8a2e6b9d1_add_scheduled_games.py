"""add scheduled_games

Revision ID: c4f8a2e6b9d1
Revises: 970a4317ccf7
Create Date: 2026-10-05 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c4f8a2e6b9d1'
down_revision: Union[str, None] = '970a4317ccf7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'scheduled_games',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('league', sa.String(length=50), nullable=False),
        sa.Column('game_date', sa.Date(), nullable=False),
        sa.Column('home_team_id', sa.Integer(), nullable=True),
        sa.Column('home_team_name', sa.String(length=100), nullable=False),
        sa.Column('away_team_id', sa.Integer(), nullable=True),
        sa.Column('away_team_name', sa.String(length=100), nullable=False),
        sa.Column('venue', sa.String(length=200), nullable=True),
        sa.Column('time_label', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['home_team_id'], ['teams.id']),
        sa.ForeignKeyConstraint(['away_team_id'], ['teams.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint(
            'league', 'game_date', 'home_team_name', 'away_team_name',
            name='uq_scheduled_game_league_date_teams',
        ),
    )
    op.create_index('ix_scheduled_games_game_date', 'scheduled_games', ['game_date'])


def downgrade() -> None:
    op.drop_index('ix_scheduled_games_game_date', table_name='scheduled_games')
    op.drop_table('scheduled_games')
