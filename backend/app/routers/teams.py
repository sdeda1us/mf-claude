from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.league_rules import compute_score
from app.models import Team, TeamSeasonResult, User
from app.schemas import TeamHistoryOut, TeamHistorySeasonOut, TeamOut
from app.team_history import TEAM_BIOS, TEAM_HISTORY_STATS, TEAM_LOCATIONS, TEAM_PROGNOSES

router = APIRouter(prefix="/teams", tags=["teams"])

# How many of a team's most recent played seasons the history page charts.
HISTORY_SEASON_COUNT = 5


@router.get("", response_model=list[TeamOut])
def list_teams(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Team).order_by(Team.league, Team.name).all()


@router.get("/{team_id}/history", response_model=TeamHistoryOut)
def get_team_history(
    team_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    """Bio, upcoming-season prognosis, and up to the last
    HISTORY_SEASON_COUNT seasons a team actually played, scored the same
    way the rest of the app scores results. The most recent season comes
    from TeamSeasonResult (live, same source Example Scores reads);
    anything older comes from the static TEAM_HISTORY_STATS reference
    data. Currently covers EPL, NFL, NBA, NHL, and URC -- other leagues
    return bio/prognosis as None and an empty season list."""
    team = db.get(Team, team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    key = (team.league, team.name)
    seasons: dict[str, dict] = dict(TEAM_HISTORY_STATS.get(key, {}))
    for result in db.query(TeamSeasonResult).filter(TeamSeasonResult.team_id == team_id):
        seasons[result.season_label] = result.stats

    recent_labels = sorted(seasons)[-HISTORY_SEASON_COUNT:]
    location = TEAM_LOCATIONS.get(key)
    return TeamHistoryOut(
        team_id=team.id,
        league=team.league,
        name=team.name,
        bio=TEAM_BIOS.get(key),
        latitude=location[0] if location else None,
        longitude=location[1] if location else None,
        prognosis=TEAM_PROGNOSES.get(key),
        seasons=[
            TeamHistorySeasonOut(season_label=label, points=compute_score(team.league, seasons[label]))
            for label in recent_labels
        ],
    )
