from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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
from app.models import Team, TeamSeasonResult, User
from app.schemas import ExampleScoreOut, LeagueRulesOut

router = APIRouter(prefix="/leagues", tags=["leagues"])


@router.get("/rules", response_model=LeagueRulesOut)
def get_rules(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    minor_conference_teams: dict[str, list[str]] = {}
    for league in MINOR_CONFERENCE_CAPS:
        minor_conference_teams[league] = [
            t.name
            for t in db.query(Team).filter(Team.league == league).all()
            if is_minor_conference_team(league, t.name)
        ]
    return LeagueRulesOut(
        roster_limits=ROSTER_LIMITS,
        scoring_rules=SCORING_RULES,
        league_session=LEAGUE_SESSION,
        minor_conference_teams=minor_conference_teams,
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
