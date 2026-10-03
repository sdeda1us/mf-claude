import secrets

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.daily_score_sync import TeamNotFoundError, UnsupportedLeagueError, sync_team_stats
from app.database import get_db
from app.models import RosterEntry, Season, SeasonStatus, Team
from app.schemas import DailySyncBatchIn, DailySyncBatchResultOut, DailySyncSkipOut

router = APIRouter(prefix="/scoring-sync", tags=["scoring-sync"])


def require_daily_sync_token(authorization: str | None = Header(default=None)) -> None:
    """Bearer-token auth for the unattended daily sync routine -- distinct
    from get_current_user's session-cookie auth, since no human logs in
    for this call. 503 (not configured) vs 401 (wrong/missing token) are
    kept separate so a misconfigured deploy is obvious from the status
    code alone."""
    expected = settings.daily_sync_token
    if not expected:
        raise HTTPException(status_code=503, detail="Daily sync not configured")
    provided = authorization.removeprefix("Bearer ") if authorization else ""
    if not authorization or not authorization.startswith("Bearer ") or not secrets.compare_digest(
        provided, expected
    ):
        raise HTTPException(status_code=401, detail="Invalid or missing token")


@router.post("/batch", response_model=DailySyncBatchResultOut)
def sync_batch(
    payload: DailySyncBatchIn,
    db: Session = Depends(get_db),
    _: None = Depends(require_daily_sync_token),
):
    """Called once a day by the scheduled cloud routine with that day's
    looked-up stats for every in-scope league. Only teams actually
    rostered under the active Season are synced -- same "only drafted
    teams" behavior app/update_live_standings.py already had, just
    enforced in code here instead of by hand-curating which teams appear
    in a dict literal."""
    active_season = db.query(Season).filter(Season.status == SeasonStatus.active).first()
    if active_season is None:
        raise HTTPException(status_code=409, detail="No active season")

    synced = 0
    skipped: list[DailySyncSkipOut] = []
    for entry in payload.entries:
        team = db.query(Team).filter(Team.league == entry.league, Team.name == entry.team).first()
        if team is None:
            skipped.append(DailySyncSkipOut(league=entry.league, team=entry.team, reason="no Team row"))
            continue
        rostered = (
            db.query(RosterEntry)
            .filter(RosterEntry.season_id == active_season.id, RosterEntry.team_id == team.id)
            .first()
        )
        if rostered is None:
            skipped.append(DailySyncSkipOut(league=entry.league, team=entry.team, reason="not rostered"))
            continue
        try:
            sync_team_stats(db, entry.league, entry.team, entry.stats)
            synced += 1
        except UnsupportedLeagueError:
            skipped.append(
                DailySyncSkipOut(league=entry.league, team=entry.team, reason="unsupported league")
            )
        except TeamNotFoundError:
            skipped.append(DailySyncSkipOut(league=entry.league, team=entry.team, reason="no Team row"))

    db.commit()
    return DailySyncBatchResultOut(synced=synced, skipped=skipped)
