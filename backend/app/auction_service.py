from datetime import datetime, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.league_rules import LEAGUE_SESSION, MINOR_CONFERENCE_CAPS, ROSTER_LIMITS, is_minor_conference_team
from app.models import (
    Auction,
    AuctionItem,
    AuctionItemStatus,
    Bid,
    QueueEntry,
    ReserveBid,
    RosterEntry,
    RosterSource,
    Season,
    Team,
    User,
    utcnow,
)
from app.schemas import AuctionItemOut, AuctionOut, AuctionStateOut, ReserveBidOut, RosterStatusOut

TOTAL_ROSTER_SLOTS = sum(ROSTER_LIMITS.values())

# Each league belongs to exactly one auction session (see
# docs/wiki/README.md's "Auction Sessions" section) — precompute both the
# leagues and the total roster-slot count per session, so the turn-strip can
# show "how many teams do I still need" scoped to whichever auction is live
# rather than the full-season total.
SESSION_LEAGUES: dict[str, list[str]] = {
    session: [league for league, s in LEAGUE_SESSION.items() if s == session]
    for session in ("fall", "spring")
}
SESSION_ROSTER_SLOTS: dict[str, int] = {
    session: sum(ROSTER_LIMITS[league] for league in leagues)
    for session, leagues in SESSION_LEAGUES.items()
}


def remaining_budget_by_user(db: Session, season: Season, session: str) -> dict[int, float]:
    """Fall and spring each draw from their own separate budget — spending
    in one session's leagues never eats into the other's, so this is
    always scoped to one session, never a whole-season total."""
    users = db.query(User).all()
    spent_by_user = dict(
        db.query(RosterEntry.user_id, func.coalesce(func.sum(RosterEntry.price_paid), 0))
        .join(Team, RosterEntry.team_id == Team.id)
        .filter(
            RosterEntry.season_id == season.id,
            Team.league.in_(SESSION_LEAGUES.get(session, [])),
        )
        .group_by(RosterEntry.user_id)
        .all()
    )
    budget = float(season.fall_budget_per_user if session == "fall" else season.spring_budget_per_user)
    return {u.id: budget - float(spent_by_user.get(u.id, 0)) for u in users}


def roster_status_by_user(db: Session, season: Season, session: str) -> dict[int, RosterStatusOut]:
    """Budget/spots info for the turn strip, scoped to whichever auction
    session is live — "teams they still need" and the resulting max safe
    bid both only count this session's leagues, not the other session's
    still-untouched roster slots."""
    users = db.query(User).all()
    budgets = remaining_budget_by_user(db, season, session)
    filled_by_user = dict(
        db.query(RosterEntry.user_id, func.count(RosterEntry.id))
        .join(Team, RosterEntry.team_id == Team.id)
        .filter(
            RosterEntry.season_id == season.id,
            Team.league.in_(SESSION_LEAGUES.get(session, [])),
        )
        .group_by(RosterEntry.user_id)
        .all()
    )
    total_slots = SESSION_ROSTER_SLOTS.get(session, TOTAL_ROSTER_SLOTS)
    status: dict[int, RosterStatusOut] = {}
    for u in users:
        spots_filled = int(filled_by_user.get(u.id, 0))
        spots_remaining = total_slots - spots_filled
        budget_remaining = budgets[u.id]
        # Leave $1 for each of this session's OTHER remaining spots after
        # this bid.
        max_bid = max(0.0, budget_remaining - max(spots_remaining - 1, 0))
        status[u.id] = RosterStatusOut(
            budget_remaining=budget_remaining,
            spots_filled=spots_filled,
            spots_remaining=spots_remaining,
            max_bid=max_bid,
        )
    return status


def get_active_item(db: Session, auction_id: int) -> AuctionItem | None:
    return (
        db.query(AuctionItem)
        .filter(
            AuctionItem.auction_id == auction_id,
            AuctionItem.status == AuctionItemStatus.active,
        )
        .first()
    )


def current_turn_user_id(db: Session, auction: Auction) -> int | None:
    if not auction.nomination_order or get_active_item(db, auction.id) is not None:
        return None
    return auction.nomination_order[len(auction.items) % len(auction.nomination_order)]


def build_state(db: Session, auction: Auction, viewer_user_id: int) -> AuctionStateOut:
    active_item = get_active_item(db, auction.id)
    active_item_out = AuctionItemOut.model_validate(active_item) if active_item else None
    if active_item_out is not None:
        # Reserves are private — only ever include the viewer's own, never
        # another user's, regardless of who else has one active.
        reserve = (
            db.query(ReserveBid)
            .filter(
                ReserveBid.auction_item_id == active_item.id,
                ReserveBid.user_id == viewer_user_id,
            )
            .first()
        )
        if reserve is not None:
            active_item_out.my_reserve = ReserveBidOut(
                amount=float(reserve.max_amount), active=reserve.active
            )
    return AuctionStateOut(
        auction=AuctionOut.model_validate(auction),
        active_item=active_item_out,
        remaining_budget_by_user=remaining_budget_by_user(db, auction.season, auction.session),
        current_turn_user_id=current_turn_user_id(db, auction),
        roster_status_by_user=roster_status_by_user(db, auction.season, auction.session),
    )


def current_high_bid(item: AuctionItem) -> float:
    if not item.bids:
        return 0.0
    return max(float(b.amount) for b in item.bids)


def high_bidder_user_id(item: AuctionItem) -> int | None:
    if not item.bids:
        return None
    return max(item.bids, key=lambda b: float(b.amount)).user_id


def all_non_high_bidders_passed(db: Session, item: AuctionItem) -> bool:
    """True once every user except the current high bidder has passed on
    this item — the early-close condition, checked after every pass."""
    winner_id = high_bidder_user_id(item)
    if winner_id is None:
        return False
    all_user_ids = {u.id for u in db.query(User).all()}
    required = all_user_ids - {winner_id}
    return required.issubset(set(item.passed_user_ids))


def _naive_utc(dt: datetime) -> datetime:
    # Mirrors auction_timer.naive_utc — duplicated rather than imported to
    # avoid a circular import (auction_timer already imports from this
    # module). SQLite/plain-TIMESTAMP columns drop tzinfo on round-trip, so
    # values coming back from the DB are naive even though written as UTC.
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def resolve_reserve_bids(
    db: Session,
    auction: Auction,
    item: AuctionItem,
    *,
    bid_extension_threshold_seconds: int,
    bid_extension_seconds: int,
) -> None:
    """After any bid changes the high bidder, auto-place bids on behalf of
    anyone with an active reserve (ReserveBid) on this item, topping the
    new high bid by $1 — repeating (a reserve's own auto-bid can trigger a
    rival reserve to respond) until no active reserve can afford to go
    higher. Each auto-bid is a real Bid row and gets the same soft-close
    deadline extension a manual bid would, so it's indistinguishable from
    one in the bid log. Call this after auto_pass_capped_users so already-
    capped users are correctly excluded."""
    league = item.team.league
    limit = ROSTER_LIMITS.get(league)
    minor_cap = MINOR_CONFERENCE_CAPS.get(league)
    is_minor = minor_cap is not None and is_minor_conference_team(league, item.team.name)

    while True:
        current_high = current_high_bid(item)
        winner_id = high_bidder_user_id(item)
        next_amount = current_high + 1

        reserves = (
            db.query(ReserveBid)
            .filter(ReserveBid.auction_item_id == item.id, ReserveBid.active.is_(True))
            .order_by(ReserveBid.max_amount.desc(), ReserveBid.created_at.asc())
            .all()
        )
        budgets = remaining_budget_by_user(db, auction.season, auction.session)

        candidate = None
        for r in reserves:
            if r.user_id == winner_id or r.user_id in item.passed_user_ids:
                continue
            if r.max_amount < next_amount:
                continue
            if next_amount > budgets.get(r.user_id, 0):
                continue
            if limit is not None and count_user_league_teams(db, auction.season_id, r.user_id, league) >= limit:
                continue
            if is_minor and count_user_minor_conference_teams(db, auction.season_id, r.user_id, league) >= minor_cap:
                continue
            candidate = r
            break

        if candidate is None:
            return

        new_bid = Bid(auction_item_id=item.id, user_id=candidate.user_id, amount=next_amount)
        item.bids.append(new_bid)
        db.add(new_bid)

        if item.bid_deadline is not None:
            now = datetime.utcnow()
            remaining_seconds = (_naive_utc(item.bid_deadline) - now).total_seconds()
            if remaining_seconds < bid_extension_threshold_seconds:
                item.bid_deadline = now + timedelta(seconds=bid_extension_seconds)


def auto_pass_capped_users(db: Session, auction: Auction, item: AuctionItem) -> None:
    """Anyone already at their roster cap for this item's league -- or, if
    this item's team is itself a minor-conference team, already at their
    separate minor-conference sub-cap -- can't legally bid on it (the WS
    bid handler already blocks both). So they're auto-passed the moment
    there's a high bidder to pass around, instead of making them click
    Pass on a team they were never eligible to win. Call this right after
    any bid is placed (the only time high_bidder_user_id is defined);
    safe to call repeatedly, already-passed users are skipped."""
    league = item.team.league
    limit = ROSTER_LIMITS.get(league)
    minor_cap = MINOR_CONFERENCE_CAPS.get(league)
    is_minor = minor_cap is not None and is_minor_conference_team(league, item.team.name)
    if limit is None and not is_minor:
        return
    winner_id = high_bidder_user_id(item)
    passed = set(item.passed_user_ids)
    changed = False
    for u in db.query(User).all():
        if u.id == winner_id or u.id in passed:
            continue
        capped_overall = limit is not None and count_user_league_teams(db, auction.season_id, u.id, league) >= limit
        capped_minor = is_minor and count_user_minor_conference_teams(db, auction.season_id, u.id, league) >= minor_cap
        if capped_overall or capped_minor:
            passed.add(u.id)
            changed = True
    if changed:
        item.passed_user_ids = list(passed)


def finalize_active_item(db: Session, auction: Auction, item: AuctionItem) -> None:
    """Marks the active item sold to its current high bidder (if any) and
    opens the next nomination turn. Shared by the manual "close" action, the
    bidding countdown running out, and everyone-but-the-high-bidder passing —
    doesn't commit or broadcast, callers do that themselves."""
    item.status = AuctionItemStatus.sold
    if item.bids:
        winner = max(item.bids, key=lambda b: float(b.amount))
        item.winning_user_id = winner.user_id
        item.winning_bid = winner.amount
        db.add(
            RosterEntry(
                season_id=auction.season_id,
                user_id=winner.user_id,
                team_id=item.team_id,
                price_paid=winner.amount,
                source=RosterSource.auction,
            )
        )
        db.query(QueueEntry).filter(
            QueueEntry.season_id == auction.season_id, QueueEntry.team_id == item.team_id
        ).delete()
    auction.turn_started_at = utcnow()


def count_user_league_teams(db: Session, season_id: int, user_id: int, league: str) -> int:
    return (
        db.query(RosterEntry)
        .join(Team, RosterEntry.team_id == Team.id)
        .filter(
            RosterEntry.season_id == season_id,
            RosterEntry.user_id == user_id,
            Team.league == league,
        )
        .count()
    )


def count_user_minor_conference_teams(db: Session, season_id: int, user_id: int, league: str) -> int:
    names = (
        db.query(Team.name)
        .join(RosterEntry, RosterEntry.team_id == Team.id)
        .filter(
            RosterEntry.season_id == season_id,
            RosterEntry.user_id == user_id,
            Team.league == league,
        )
        .all()
    )
    return sum(1 for (name,) in names if is_minor_conference_team(league, name))
