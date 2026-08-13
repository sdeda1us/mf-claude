from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auction_service import build_state
from app.database import get_db
from app.deps import get_current_commissioner, get_current_user
from app.models import Auction, RosterEntry, RosterSource, Season, Team, User
from app.schemas import RosterCorrectionIn, RosterEntryOut
from app.ws.connection_manager import manager

router = APIRouter(prefix="/seasons/{season_id}/roster", tags=["roster"])


@router.get("", response_model=list[RosterEntryOut])
def list_roster(
    season_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    return (
        db.query(RosterEntry)
        .filter(RosterEntry.season_id == season_id)
        .order_by(RosterEntry.user_id)
        .all()
    )


@router.get("/me", response_model=list[RosterEntryOut])
def my_roster(
    season_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return (
        db.query(RosterEntry)
        .filter(RosterEntry.season_id == season_id, RosterEntry.user_id == user.id)
        .all()
    )


@router.post("/correction", response_model=RosterEntryOut, status_code=201)
def correct_roster(
    season_id: int,
    payload: RosterCorrectionIn,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_commissioner),
):
    if db.get(Season, season_id) is None:
        raise HTTPException(status_code=404, detail="Season not found")
    if db.get(Team, payload.team_id) is None:
        raise HTTPException(status_code=404, detail="Team not found")
    if db.get(User, payload.user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")

    entry = RosterEntry(
        season_id=season_id,
        user_id=payload.user_id,
        team_id=payload.team_id,
        price_paid=payload.price_paid,
        source=RosterSource.commissioner_correction,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{roster_entry_id}", status_code=204)
async def rollback_roster_entry(
    season_id: int,
    roster_entry_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_commissioner),
):
    """Undo a pick: removes the team from the owner's roster and returns it
    to the draftable pool. The budget spent on it is refunded automatically,
    since remaining budget is always computed live from RosterEntry rows —
    nothing else to update there."""
    entry = (
        db.query(RosterEntry)
        .filter(RosterEntry.id == roster_entry_id, RosterEntry.season_id == season_id)
        .first()
    )
    if entry is None:
        raise HTTPException(status_code=404, detail="Roster entry not found")

    db.delete(entry)
    db.commit()

    auction = (
        db.query(Auction)
        .filter(Auction.season_id == season_id)
        .order_by(Auction.created_at.desc())
        .first()
    )
    if auction is not None:
        state = build_state(db, auction)
        await manager.broadcast_state(auction.id, state)
