import random
from datetime import timedelta
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auction_service import (
    build_state,
    count_user_league_teams,
    count_user_minor_conference_teams,
    current_turn_user_id,
    finalize_active_item,
    get_active_item,
)
from app.auction_timer import (
    BID_TIMEOUT_SECONDS,
    naive_utc,
    schedule_bid_timer,
    schedule_turn_timer,
)
from app.database import get_db
from app.deps import get_current_commissioner, get_current_user
from app.league_rules import LEAGUE_SESSION, MINOR_CONFERENCE_CAPS, ROSTER_LIMITS, is_minor_conference_team
from app.models import (
    Auction,
    AuctionItem,
    AuctionItemStatus,
    AuctionStatus,
    Season,
    Team,
    User,
    utcnow,
)
from app.schemas import AuctionOut, AuctionStateOut, ForceTurnIn, NominateIn
from app.ws.connection_manager import manager

router = APIRouter(prefix="/auctions", tags=["auction"])

AuctionSession = Literal["fall", "spring"]


@router.post("/seasons/{season_id}", response_model=AuctionOut, status_code=201)
async def create_auction(
    season_id: int,
    session: AuctionSession = "fall",
    db: Session = Depends(get_db),
    _: User = Depends(get_current_commissioner),
):
    if db.get(Season, season_id) is None:
        raise HTTPException(status_code=404, detail="Season not found")
    user_ids = [u.id for u in db.query(User).all()]
    random.shuffle(user_ids)
    auction = Auction(
        season_id=season_id, session=session, status=AuctionStatus.pending, nomination_order=user_ids
    )
    db.add(auction)
    db.commit()
    db.refresh(auction)
    manager.spawn(schedule_turn_timer(auction.id))
    return auction


@router.get("/seasons/{season_id}", response_model=AuctionOut | None)
def get_auction_for_season(
    season_id: int,
    session: AuctionSession = "fall",
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return (
        db.query(Auction)
        .filter(Auction.season_id == season_id, Auction.session == session)
        .order_by(Auction.created_at.desc())
        .first()
    )


@router.get("/{auction_id}/state", response_model=AuctionStateOut)
def get_state(
    auction_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    auction = db.get(Auction, auction_id)
    if auction is None:
        raise HTTPException(status_code=404, detail="Auction not found")
    return build_state(db, auction, viewer_user_id=user.id)


@router.post("/{auction_id}/nominate", response_model=AuctionStateOut)
async def nominate(
    auction_id: int,
    payload: NominateIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    auction = db.get(Auction, auction_id)
    if auction is None:
        raise HTTPException(status_code=404, detail="Auction not found")
    if auction.is_paused:
        raise HTTPException(status_code=409, detail="Auction is paused")
    if get_active_item(db, auction_id) is not None:
        raise HTTPException(status_code=400, detail="An item is already active")
    if not user.is_commissioner and user.id != current_turn_user_id(db, auction):
        raise HTTPException(status_code=403, detail="It's not your turn to nominate")
    team = db.get(Team, payload.team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    if LEAGUE_SESSION.get(team.league) != auction.session:
        raise HTTPException(
            status_code=400,
            detail=f"{team.league} isn't part of the {auction.session} session",
        )
    # Nominating always pairs with the nominator's own opening bid (the
    # frontend fires it immediately after), so someone who couldn't
    # legally roster this team themselves shouldn't be able to nominate it
    # either -- otherwise the item opens with no valid opening bid and
    # just sits there.
    limit = ROSTER_LIMITS.get(team.league)
    if limit is not None and count_user_league_teams(db, auction.season_id, user.id, team.league) >= limit:
        raise HTTPException(
            status_code=400,
            detail=f"You already own the maximum number of {team.league} teams ({limit})",
        )
    minor_cap = MINOR_CONFERENCE_CAPS.get(team.league)
    if minor_cap is not None and is_minor_conference_team(team.league, team.name):
        if count_user_minor_conference_teams(db, auction.season_id, user.id, team.league) >= minor_cap:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"You already own the maximum number of minor-conference {team.league} "
                    f"teams ({minor_cap})"
                ),
            )

    next_order = len(auction.items)
    item = AuctionItem(
        auction_id=auction_id,
        team_id=payload.team_id,
        order=next_order,
        status=AuctionItemStatus.active,
        bid_deadline=utcnow() + timedelta(seconds=BID_TIMEOUT_SECONDS),
    )
    auction.status = AuctionStatus.live
    db.add(item)
    db.commit()
    db.refresh(auction)
    db.refresh(item)
    await manager.broadcast_state(auction_id, db, auction)
    manager.spawn(schedule_bid_timer(item.id))
    return build_state(db, auction, viewer_user_id=user.id)


@router.post("/{auction_id}/force-turn", response_model=AuctionStateOut)
async def force_turn(
    auction_id: int,
    payload: ForceTurnIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_commissioner),
):
    """Commissioner override: makes it the given user's turn to nominate
    right now, by swapping them into the current slot of nomination_order
    with whoever's sitting there. That keeps nomination_order a permutation
    of every user (current_turn_user_id just indexes into it), so nobody's
    future turn is lost — the bumped user simply inherits the forced user's
    old slot and comes up in their place next cycle. Only valid while
    there's an open turn to hand off (no active item)."""
    auction = db.get(Auction, auction_id)
    if auction is None:
        raise HTTPException(status_code=404, detail="Auction not found")
    if get_active_item(db, auction_id) is not None:
        raise HTTPException(status_code=400, detail="An item is already active")
    if not auction.nomination_order:
        raise HTTPException(status_code=400, detail="Auction has no nomination order")
    if payload.user_id not in auction.nomination_order:
        raise HTTPException(status_code=404, detail="That user isn't part of this auction")

    order = list(auction.nomination_order)
    current_index = len(auction.items) % len(order)
    target_index = order.index(payload.user_id)
    order[current_index], order[target_index] = order[target_index], order[current_index]
    auction.nomination_order = order
    db.commit()
    db.refresh(auction)
    await manager.broadcast_state(auction_id, db, auction)
    # turn_started_at is untouched (same slot, same clock) but the running
    # schedule_turn_timer captured the old turn's user id before it started
    # sleeping — it'll now no-op at fire time since current_turn_user_id
    # moved out from under it, so re-arm a fresh one for the new user.
    manager.spawn(schedule_turn_timer(auction_id))
    return build_state(db, auction, viewer_user_id=user.id)


@router.post("/{auction_id}/cancel-nomination", response_model=AuctionStateOut)
async def cancel_nomination(
    auction_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_commissioner),
):
    """Undo the current nomination: removes the active item and every bid on
    it, returning the team to the pool. Nothing needs to be done to restore
    whose turn it is — that's derived from how many items have been
    nominated so far, so removing this one automatically hands the turn
    back to whoever nominated it."""
    auction = db.get(Auction, auction_id)
    if auction is None:
        raise HTTPException(status_code=404, detail="Auction not found")
    item = get_active_item(db, auction_id)
    if item is None:
        raise HTTPException(status_code=400, detail="No active nomination to cancel")

    for bid in item.bids:
        db.delete(bid)
    db.delete(item)
    auction.turn_started_at = utcnow()
    db.commit()
    db.refresh(auction)
    await manager.broadcast_state(auction_id, db, auction)
    manager.spawn(schedule_turn_timer(auction_id))
    return build_state(db, auction, viewer_user_id=user.id)


@router.post("/{auction_id}/close", response_model=AuctionStateOut)
async def close_item(
    auction_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_commissioner),
):
    auction = db.get(Auction, auction_id)
    if auction is None:
        raise HTTPException(status_code=404, detail="Auction not found")
    item = get_active_item(db, auction_id)
    if item is None:
        raise HTTPException(status_code=400, detail="No active item to close")

    finalize_active_item(db, auction, item)
    db.commit()
    db.refresh(auction)
    await manager.broadcast_state(auction_id, db, auction)
    manager.spawn(schedule_turn_timer(auction_id))
    return build_state(db, auction, viewer_user_id=user.id)


@router.post("/{auction_id}/pause", response_model=AuctionStateOut)
async def pause_auction(
    auction_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_commissioner),
):
    auction = db.get(Auction, auction_id)
    if auction is None:
        raise HTTPException(status_code=404, detail="Auction not found")
    if not auction.is_paused:
        auction.is_paused = True
        auction.paused_at = utcnow()
        db.commit()
        db.refresh(auction)
    await manager.broadcast_state(auction_id, db, auction)
    return build_state(db, auction, viewer_user_id=user.id)


@router.post("/{auction_id}/resume", response_model=AuctionStateOut)
async def resume_auction(
    auction_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_commissioner),
):
    """Unpause: shifts whichever deadline was running (the nomination clock,
    or the active item's bidding clock) forward by exactly how long the
    pause lasted, so time spent paused is never held against anyone, then
    re-arms a fresh timer for whatever's left."""
    auction = db.get(Auction, auction_id)
    if auction is None:
        raise HTTPException(status_code=404, detail="Auction not found")
    if auction.is_paused and auction.paused_at is not None:
        elapsed = naive_utc(utcnow()) - naive_utc(auction.paused_at)
        item = get_active_item(db, auction_id)
        if item is not None and item.bid_deadline is not None:
            item.bid_deadline = naive_utc(item.bid_deadline) + elapsed
        elif current_turn_user_id(db, auction) is not None:
            auction.turn_started_at = naive_utc(auction.turn_started_at) + elapsed
        auction.is_paused = False
        auction.paused_at = None
        db.commit()
        db.refresh(auction)

        item = get_active_item(db, auction_id)
        if item is not None:
            manager.spawn(schedule_bid_timer(item.id))
        elif current_turn_user_id(db, auction) is not None:
            manager.spawn(schedule_turn_timer(auction_id))

    await manager.broadcast_state(auction_id, db, auction)
    return build_state(db, auction, viewer_user_id=user.id)
