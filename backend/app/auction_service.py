from sqlalchemy import func
from sqlalchemy.orm import Session

from app.league_rules import LEAGUE_SESSION, ROSTER_LIMITS, is_minor_conference_team
from app.models import (
    Auction,
    AuctionItem,
    AuctionItemStatus,
    QueueEntry,
    RosterEntry,
    RosterSource,
    Season,
    Team,
    User,
    utcnow,
)
from app.schemas import AuctionItemOut, AuctionOut, AuctionStateOut, RosterStatusOut

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


def remaining_budget_by_user(db: Session, season: Season) -> dict[int, float]:
    users = db.query(User).all()
    spent_by_user = dict(
        db.query(RosterEntry.user_id, func.coalesce(func.sum(RosterEntry.price_paid), 0))
        .filter(RosterEntry.season_id == season.id)
        .group_by(RosterEntry.user_id)
        .all()
    )
    budget = float(season.budget_per_user)
    return {u.id: budget - float(spent_by_user.get(u.id, 0)) for u in users}


def roster_status_by_user(db: Session, season: Season, session: str) -> dict[int, RosterStatusOut]:
    """Budget/spots info for the turn strip, scoped to whichever auction
    session is live — "teams they still need" and the resulting max safe
    bid both only count this session's leagues, not the other session's
    still-untouched roster slots."""
    users = db.query(User).all()
    budgets = remaining_budget_by_user(db, season)
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


def build_state(db: Session, auction: Auction) -> AuctionStateOut:
    active_item = get_active_item(db, auction.id)
    return AuctionStateOut(
        auction=AuctionOut.model_validate(auction),
        active_item=AuctionItemOut.model_validate(active_item) if active_item else None,
        remaining_budget_by_user=remaining_budget_by_user(db, auction.season),
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


def auto_pass_capped_users(db: Session, auction: Auction, item: AuctionItem) -> None:
    """Anyone already at their roster cap for this item's league can't
    legally bid on it — the WS bid handler already blocks them — so they're
    auto-passed the moment there's a high bidder to pass around, instead of
    making them click Pass on a team they were never eligible to win. Call
    this right after any bid is placed (the only time high_bidder_user_id
    is defined); safe to call repeatedly, already-passed users are skipped."""
    league = item.team.league
    limit = ROSTER_LIMITS.get(league)
    if limit is None:
        return
    winner_id = high_bidder_user_id(item)
    passed = set(item.passed_user_ids)
    changed = False
    for u in db.query(User).all():
        if u.id == winner_id or u.id in passed:
            continue
        if count_user_league_teams(db, auction.season_id, u.id, league) >= limit:
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
