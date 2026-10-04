from datetime import timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.daily_score_sync import today_eastern
from app.database import get_db
from app.deps import get_current_user
from app.league_rules import (
    LEAGUE_SESSION,
    MINOR_CONFERENCE_CAPS,
    ROSTER_LIMITS,
    SCORING_RULES,
    compute_score,
    compute_score_breakdown,
    is_minor_conference_team,
)
from app.models import Team, TeamDailyScore, TeamSeasonResult, User
from app.schemas import ExampleScoreOut, LeagueRulesOut

router = APIRouter(prefix="/leagues", tags=["leagues"])

# A league counts as "active" (actively being scored right now, as
# opposed to merely in the daily sync's 9-league scope) if it has a
# TeamDailyScore row dated within this many days -- covers the gap
# between the routine researching a day's stats and the backend's own
# pull picking them up (see app/daily_sync_pull.py) without needing any
# hardcoded real-world season date ranges.
ACTIVE_LEAGUE_LOOKBACK_DAYS = 2


@router.get("/rules", response_model=LeagueRulesOut)
def get_rules(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    minor_conference_teams: dict[str, list[str]] = {}
    for league in MINOR_CONFERENCE_CAPS:
        minor_conference_teams[league] = [
            t.name
            for t in db.query(Team).filter(Team.league == league).all()
            if is_minor_conference_team(league, t.name)
        ]

    cutoff = today_eastern() - timedelta(days=ACTIVE_LEAGUE_LOOKBACK_DAYS)
    active_leagues = sorted(
        {
            row[0]
            for row in db.query(TeamDailyScore.league)
            .filter(TeamDailyScore.as_of_date >= cutoff)
            .distinct()
            .all()
        }
    )

    return LeagueRulesOut(
        roster_limits=ROSTER_LIMITS,
        scoring_rules=SCORING_RULES,
        league_session=LEAGUE_SESSION,
        minor_conference_teams=minor_conference_teams,
        active_leagues=active_leagues,
    )


@router.get("/example-scores", response_model=list[ExampleScoreOut])
def get_example_scores(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    results = db.query(TeamSeasonResult).all()
    # A league removed from the app (e.g. a swap like IndyCar -> NWSL) can
    # leave behind a TeamSeasonResult row for a team whose historical
    # RosterEntry/AuctionItem references block it from being cleaned up —
    # compute_score no longer recognizes that league, so skip rather than
    # let one stale row 500 the whole page for everyone.
    return [
        ExampleScoreOut(
            team_id=r.team_id,
            team_name=r.team.name,
            league=r.league,
            season_label=r.season_label,
            points=compute_score(r.league, r.stats),
            breakdown=compute_score_breakdown(r.league, r.stats),
        )
        for r in results
        if r.league in ROSTER_LIMITS
    ]
