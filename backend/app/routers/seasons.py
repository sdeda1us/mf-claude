from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_commissioner, get_current_user
from app.models import (
    Auction,
    AuctionItem,
    Bid,
    QueueEntry,
    ReserveBid,
    RosterEntry,
    Season,
    SeasonStatus,
    User,
)
from app.schemas import SeasonCreateIn, SeasonOut

router = APIRouter(prefix="/seasons", tags=["seasons"])


@router.get("", response_model=list[SeasonOut])
def list_seasons(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Season).order_by(Season.created_at.desc()).all()


@router.post("", response_model=SeasonOut, status_code=201)
def create_season(
    payload: SeasonCreateIn,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_commissioner),
):
    season = Season(
        name=payload.name,
        fall_budget_per_user=payload.fall_budget_per_user,
        spring_budget_per_user=payload.spring_budget_per_user,
    )
    db.add(season)
    db.commit()
    db.refresh(season)
    return season


@router.post("/{season_id}/activate", response_model=SeasonOut)
def activate_season(
    season_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_commissioner),
):
    """Marks this the active season (the one Home.tsx shows snapshots for)
    and demotes whichever season previously held that status to "complete"
    -- only one season is ever *the* active one, and a newly-activated
    season superseding another reads truer as that other one being done
    than as it reverting to "setup"."""
    season = db.get(Season, season_id)
    if season is None:
        raise HTTPException(status_code=404, detail="Season not found")

    db.query(Season).filter(Season.status == SeasonStatus.active, Season.id != season_id).update(
        {"status": SeasonStatus.complete}, synchronize_session=False
    )
    season.status = SeasonStatus.active
    db.commit()
    db.refresh(season)
    return season


@router.delete("/{season_id}", status_code=204)
def delete_season(
    season_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_commissioner),
):
    """Permanently deletes a season and everything scoped to it -- rosters,
    the queue, and every auction (with its items, bids, and reserve bids).
    Meant for cleaning up old test seasons; there's no undo, so the
    frontend confirms before calling this.

    CribSheetEntry and TeamSeasonResult are deliberately untouched: neither
    is season-scoped (a crib sheet value is a player's opinion of a team in
    general, and historical results are keyed by the real-world league
    season, not this app's Season row)."""
    season = db.get(Season, season_id)
    if season is None:
        raise HTTPException(status_code=404, detail="Season not found")

    auction_ids = [row[0] for row in db.query(Auction.id).filter(Auction.season_id == season_id).all()]
    if auction_ids:
        item_ids = [
            row[0]
            for row in db.query(AuctionItem.id).filter(AuctionItem.auction_id.in_(auction_ids)).all()
        ]
        if item_ids:
            db.query(Bid).filter(Bid.auction_item_id.in_(item_ids)).delete(synchronize_session=False)
            db.query(ReserveBid).filter(ReserveBid.auction_item_id.in_(item_ids)).delete(
                synchronize_session=False
            )
            db.query(AuctionItem).filter(AuctionItem.id.in_(item_ids)).delete(synchronize_session=False)
        db.query(Auction).filter(Auction.id.in_(auction_ids)).delete(synchronize_session=False)

    db.query(QueueEntry).filter(QueueEntry.season_id == season_id).delete(synchronize_session=False)
    db.query(RosterEntry).filter(RosterEntry.season_id == season_id).delete(synchronize_session=False)

    db.delete(season)
    db.commit()
