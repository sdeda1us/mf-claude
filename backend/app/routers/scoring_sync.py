import secrets

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.daily_score_sync import NoActiveSeasonError, apply_daily_sync_batch
from app.database import get_db
from app.schemas import DailySyncBatchIn, DailySyncBatchResultOut

router = APIRouter(prefix="/scoring-sync", tags=["scoring-sync"])


def require_daily_sync_token(authorization: str | None = Header(default=None)) -> None:
    """Bearer-token auth for a manual/direct call to this endpoint --
    distinct from get_current_user's session-cookie auth, since no human
    logs in for this call. The scheduled daily routine no longer calls
    this directly (see app/daily_sync_pull.py's docstring for why), but
    this stays available for manual testing or an alternate caller. 503
    (not configured) vs 401 (wrong/missing token) are kept separate so a
    misconfigured deploy is obvious from the status code alone."""
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
    try:
        result = apply_daily_sync_batch(db, payload.entries)
    except NoActiveSeasonError:
        raise HTTPException(status_code=409, detail="No active season")
    db.commit()
    return result
