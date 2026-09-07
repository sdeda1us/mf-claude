from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auction_service import effective_crib_value
from app.database import get_db
from app.deps import get_current_user
from app.models import QueueEntry, RosterEntry, Season, Team, User
from app.schemas import (
    QueueAddIn,
    QueueEntryOut,
    QueueMoveIn,
    QueueNominationPriceIn,
    QueueReservePriceIn,
)

router = APIRouter(prefix="/seasons/{season_id}/queue", tags=["queue"])


def _ordered_queue(db: Session, season_id: int, user_id: int) -> list[QueueEntry]:
    return (
        db.query(QueueEntry)
        .filter(QueueEntry.season_id == season_id, QueueEntry.user_id == user_id)
        .order_by(QueueEntry.order, QueueEntry.id)
        .all()
    )


def _get_owned_entry(db: Session, season_id: int, entry_id: int, user_id: int) -> QueueEntry:
    entry = (
        db.query(QueueEntry)
        .filter(
            QueueEntry.id == entry_id,
            QueueEntry.season_id == season_id,
            QueueEntry.user_id == user_id,
        )
        .first()
    )
    if entry is None:
        raise HTTPException(status_code=404, detail="Queue entry not found")
    return entry


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
        # Starting point for the reserve price this team will bid up to once
        # it's nominated (by anyone) and applied automatically — same crib
        # sheet value shown everywhere else, fully editable from here on.
        reserve_price=effective_crib_value(db, user.id, payload.team_id),
        # Starting point for the opening bid placed when *this* player
        # nominates the team — the app's long-standing $1 convention,
        # fully editable from here on.
        nomination_price=1,
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
    entry = _get_owned_entry(db, season_id, entry_id, user.id)
    db.delete(entry)
    db.commit()


@router.put("/{entry_id}/reserve-price", response_model=QueueEntryOut)
def set_queue_reserve_price(
    season_id: int,
    entry_id: int,
    payload: QueueReservePriceIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    entry = _get_owned_entry(db, season_id, entry_id, user.id)
    if payload.reserve_price is not None and payload.reserve_price <= 0:
        raise HTTPException(status_code=400, detail="Reserve price must be greater than 0")
    entry.reserve_price = payload.reserve_price
    db.commit()
    db.refresh(entry)
    return entry


@router.put("/{entry_id}/nomination-price", response_model=QueueEntryOut)
def set_queue_nomination_price(
    season_id: int,
    entry_id: int,
    payload: QueueNominationPriceIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    entry = _get_owned_entry(db, season_id, entry_id, user.id)
    if payload.nomination_price is not None and payload.nomination_price <= 0:
        raise HTTPException(status_code=400, detail="Nomination price must be greater than 0")
    entry.nomination_price = payload.nomination_price
    db.commit()
    db.refresh(entry)
    return entry


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
