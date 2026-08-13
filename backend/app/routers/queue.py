from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import QueueEntry, RosterEntry, Season, Team, User
from app.schemas import QueueAddIn, QueueEntryOut, QueueMoveIn

router = APIRouter(prefix="/seasons/{season_id}/queue", tags=["queue"])


def _ordered_queue(db: Session, season_id: int, user_id: int) -> list[QueueEntry]:
    return (
        db.query(QueueEntry)
        .filter(QueueEntry.season_id == season_id, QueueEntry.user_id == user_id)
        .order_by(QueueEntry.order, QueueEntry.id)
        .all()
    )


@router.get("", response_model=list[QueueEntryOut])
def list_queue(
    season_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return _ordered_queue(db, season_id, user.id)


@router.post("", response_model=QueueEntryOut, status_code=201)
def add_to_queue(
    season_id: int,
    payload: QueueAddIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if db.get(Season, season_id) is None:
        raise HTTPException(status_code=404, detail="Season not found")
    if db.get(Team, payload.team_id) is None:
        raise HTTPException(status_code=404, detail="Team not found")

    sold = (
        db.query(RosterEntry)
        .filter(RosterEntry.season_id == season_id, RosterEntry.team_id == payload.team_id)
        .first()
    )
    if sold is not None:
        raise HTTPException(status_code=400, detail="That team has already been sold")

    existing = (
        db.query(QueueEntry)
        .filter(
            QueueEntry.season_id == season_id,
            QueueEntry.user_id == user.id,
            QueueEntry.team_id == payload.team_id,
        )
        .first()
    )
    if existing is not None:
        return existing

    # Base the new order on the highest one in use, not the entry count —
    # removals (including the auto-nominate timer consuming the top of the
    # queue) leave gaps, and count-based numbering can hand out a value that
    # collides with an entry still in the list.
    existing_orders = [e.order for e in _ordered_queue(db, season_id, user.id)]
    entry = QueueEntry(
        season_id=season_id,
        user_id=user.id,
        team_id=payload.team_id,
        order=(max(existing_orders) + 1) if existing_orders else 0,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}", status_code=204)
def remove_from_queue(
    season_id: int,
    entry_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    entry = (
        db.query(QueueEntry)
        .filter(
            QueueEntry.id == entry_id,
            QueueEntry.season_id == season_id,
            QueueEntry.user_id == user.id,
        )
        .first()
    )
    if entry is None:
        raise HTTPException(status_code=404, detail="Queue entry not found")
    db.delete(entry)
    db.commit()


@router.post("/{entry_id}/move", response_model=list[QueueEntryOut])
def move_queue_entry(
    season_id: int,
    entry_id: int,
    payload: QueueMoveIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    entries = _ordered_queue(db, season_id, user.id)
    idx = next((i for i, e in enumerate(entries) if e.id == entry_id), None)
    if idx is None:
        raise HTTPException(status_code=404, detail="Queue entry not found")

    swap_idx = idx - 1 if payload.direction == "up" else idx + 1
    if 0 <= swap_idx < len(entries):
        entries[idx], entries[swap_idx] = entries[swap_idx], entries[idx]

    # Renumber to contiguous 0..n-1 on every move rather than just swapping
    # the two `order` values in place — that swap is a no-op whenever two
    # entries already share an order value (which happened before the
    # add-to-queue numbering fix), so this also self-heals old data.
    for i, e in enumerate(entries):
        e.order = i
    db.commit()

    return entries
