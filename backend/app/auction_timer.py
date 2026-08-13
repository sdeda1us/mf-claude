import asyncio
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.auction_service import (
    all_non_high_bidders_passed,
    auto_pass_capped_users,
    build_state,
    current_turn_user_id,
    finalize_active_item,
    get_active_item,
)
from app.database import SessionLocal
from app.league_rules import LEAGUE_SESSION, compute_score
from app.models import (
    Auction,
    AuctionItem,
    AuctionItemStatus,
    Bid,
    QueueEntry,
    RosterEntry,
    Team,
    TeamSeasonResult,
)
from app.ws.connection_manager import manager

NOMINATION_TIMEOUT_SECONDS = 3 * 60 * 60  # 3 hours
BID_TIMEOUT_SECONDS = 8 * 60 * 60  # 8 hours
BID_EXTENSION_THRESHOLD_SECONDS = 10 * 60  # 10 minutes
BID_EXTENSION_SECONDS = 10 * 60  # 10 minutes


def naive_utc(dt: datetime) -> datetime:
    # SQLite (and a plain TIMESTAMP column on Postgres) drops tzinfo on
    # round-trip, so values coming back from the DB are naive even though
    # they were written as UTC — normalize both sides before subtracting.
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


async def schedule_turn_timer(auction_id: int) -> None:
    """Give the player on the clock NOMINATION_TIMEOUT_SECONDS (from when
    their turn opened, not from when this was called) to nominate. If nobody
    has nominated by the time it fires, auto-nominate on their behalf: the
    top team on their queue, or if their queue is empty (or everything in it
    has already sold), whichever still-available team scored the most last
    season — either way opened with a $1 bid, same as a manual nominate.

    Measuring from turn_started_at rather than sleeping a flat duration
    matters for the case where this is scheduled well after the turn
    actually opened — e.g. on server startup, re-arming timers for turns
    that were already in progress before the restart."""
    db = SessionLocal()
    try:
        auction = db.get(Auction, auction_id)
        if auction is None:
            return
        turn_user_id = current_turn_user_id(db, auction)
        if turn_user_id is None:
            return
        items_at_schedule_time = len(auction.items)
        elapsed = (datetime.utcnow() - naive_utc(auction.turn_started_at)).total_seconds()
    finally:
        db.close()

    await asyncio.sleep(max(0.0, NOMINATION_TIMEOUT_SECONDS - elapsed))

    db = SessionLocal()
    try:
        auction = db.get(Auction, auction_id)
        if auction is None:
            return
        # Any of these mean the turn already moved on during the countdown —
        # nothing to do.
        if get_active_item(db, auction.id) is not None:
            return
        if len(auction.items) != items_at_schedule_time:
            return
        if current_turn_user_id(db, auction) != turn_user_id:
            return
        if auction.is_paused:
            # Frozen — resume() re-arms a fresh timer once unpaused.
            return

        team = _pick_auto_nominate_team(db, auction, turn_user_id)
        if team is None:
            return

        item = AuctionItem(
            auction_id=auction.id,
            team_id=team.id,
            order=len(auction.items),
            status=AuctionItemStatus.active,
            bid_deadline=datetime.utcnow() + timedelta(seconds=BID_TIMEOUT_SECONDS),
        )
        db.add(item)
        db.flush()
        opening_bid = Bid(auction_item_id=item.id, user_id=turn_user_id, amount=1)
        item.bids.append(opening_bid)
        db.add(opening_bid)
        db.query(QueueEntry).filter(
            QueueEntry.season_id == auction.season_id,
            QueueEntry.user_id == turn_user_id,
            QueueEntry.team_id == team.id,
        ).delete()
        # Anyone already at their roster cap for this league can't bid on
        # it, so they're auto-passed immediately — if that means literally
        # everyone else is already passed, the team sells outright rather
        # than sitting open with a countdown nobody left can act on.
        auto_pass_capped_users(db, auction, item)
        sold_immediately = all_non_high_bidders_passed(db, item)
        if sold_immediately:
            finalize_active_item(db, auction, item)
        db.commit()
        db.refresh(auction)
        db.refresh(item)
        state = build_state(db, auction)
    finally:
        db.close()

    await manager.broadcast_state(auction.id, state)
    if sold_immediately:
        manager.spawn(schedule_turn_timer(auction.id))
    else:
        manager.spawn(schedule_bid_timer(item.id))


async def schedule_bid_timer(item_id: int) -> None:
    """Close bidding on an active item once its deadline passes. Loops
    rather than sleeping once: a bid placed with under
    BID_EXTENSION_THRESHOLD_SECONDS left pushes item.bid_deadline forward
    while this may already be asleep, so on waking it re-checks the live
    deadline and, if it moved, sleeps again for the new remaining time
    instead of closing early."""
    while True:
        db = SessionLocal()
        try:
            item = db.get(AuctionItem, item_id)
            if item is None or item.status != AuctionItemStatus.active or item.bid_deadline is None:
                return
            deadline = item.bid_deadline
        finally:
            db.close()

        remaining = (deadline - datetime.utcnow()).total_seconds()
        if remaining > 0:
            await asyncio.sleep(remaining)

        db = SessionLocal()
        try:
            item = db.get(AuctionItem, item_id)
            if item is None or item.status != AuctionItemStatus.active:
                return
            auction = db.get(Auction, item.auction_id)
            if auction is None:
                return
            if auction.is_paused:
                # Frozen — resume() re-arms a fresh timer once unpaused.
                return
            if item.bid_deadline != deadline:
                continue  # extended while we slept; wait out the new time

            finalize_active_item(db, auction, item)
            db.commit()
            db.refresh(auction)
            state = build_state(db, auction)
        finally:
            db.close()

        await manager.broadcast_state(auction.id, state)
        manager.spawn(schedule_turn_timer(auction.id))
        return


def _pick_auto_nominate_team(db: Session, auction: Auction, user_id: int) -> Team | None:
    sold_team_ids = {
        row[0]
        for row in db.query(RosterEntry.team_id)
        .filter(RosterEntry.season_id == auction.season_id)
        .all()
    }

    def in_session(league: str) -> bool:
        return LEAGUE_SESSION.get(league) == auction.session

    queue = (
        db.query(QueueEntry)
        .filter(QueueEntry.season_id == auction.season_id, QueueEntry.user_id == user_id)
        .order_by(QueueEntry.order, QueueEntry.id)
        .all()
    )
    for entry in queue:
        # A player can queue teams for a session that isn't live yet, so a
        # queued team may well belong to the *other* session's auction —
        # skip those rather than letting them jump the queue for whichever
        # auction happens to be timing out right now.
        if entry.team_id not in sold_team_ids and in_session(entry.team.league):
            return entry.team

    best_team: Team | None = None
    best_score: float | None = None
    for result in db.query(TeamSeasonResult).all():
        if result.team_id in sold_team_ids or not in_session(result.league):
            continue
        score = compute_score(result.league, result.stats)
        if best_score is None or score > best_score:
            best_score = score
            best_team = result.team
    if best_team is not None:
        return best_team

    # Nothing queued and no historical data for anything left in the pool —
    # grab any remaining in-session team so the clock doesn't stall the
    # whole auction.
    for t in db.query(Team).all():
        if t.id not in sold_team_ids and in_session(t.league):
            return t
    return None
