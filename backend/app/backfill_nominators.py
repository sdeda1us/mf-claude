"""One-off backfill for AuctionItem.nominated_by_user_id on items created
before that column existed (every item sold before 2026-10-03). Every item
nominated from here on records this live at creation time (see nominate()
in routers/auction.py and the auto-nominate path in auction_timer.py) --
this script is NOT meant to be re-run as part of normal operation, only
once, right after the migration that added the column.

Why this can't just read the auction's current nomination_order: that
array is mutated in place by skip_full_players_turn (a full player gets
swapped out of the way) and by force_turn (commissioner override), so the
array as it stands today is NOT the array that was in effect when an
EARLIER item was nominated -- naively indexing into today's array for a
historical item would misattribute any item whose slot was later
swapped.

Instead, for each auction this replays the exact same skip_full_players_turn
algorithm forward, item by item, starting from a known-good anchor (the
order as it stood right when the item at START_ORDER was about to be
nominated), applying each item's REAL recorded winner/league to the
running per-user filled-spot count exactly as it happened historically.
Auctions where skip_full_players_turn never actually performed a swap
during the window being backfilled don't need an anchor -- the current
order is already the original one, so this reduces to the plain formula.

The one anchor needed: this app's only auction where a swap has ever
actually fired is auction id 3 (fall, season 2) -- I manually ran
skip_full_players_turn against it on 2026-10-03 once, at a moment captured
mid-conversation: nomination_order was [6, 2, 7, 3, 5, 4] with exactly 229
items already sold (items 0-228 were all created before the skip-logic
existed at all, so the plain formula with the PRE-swap order [6, 3, 7, 2,
5, 4] is correct for those -- nothing could have swapped them yet).
"""

from app.database import SessionLocal
from app.league_rules import LEAGUE_SESSION, ROSTER_LIMITS
from app.models import Auction, AuctionItem

SESSION_ROSTER_SLOTS = {
    session: sum(limit for league, limit in ROSTER_LIMITS.items() if LEAGUE_SESSION.get(league) == session)
    for session in ("fall", "spring")
}

# auction_id -> (anchor_order, anchor_item_order). Items before
# anchor_item_order use anchor_order directly via the plain formula (no
# replay needed, since it was the ORIGINAL unswapped order up to that
# point). Items from anchor_item_order onward are replayed forward from
# anchor_order.
ANCHORS: dict[int, tuple[list[int], int]] = {
    3: ([6, 3, 7, 2, 5, 4], 229),
}
# Auction 3's order 229-onward replay starts from the post-manual-swap
# state, not the pre-swap one above -- see backfill_auction below, which
# special-cases this by re-deriving the plain order first, then switching
# to the real anchor at the transition point.
POST_SWAP_ANCHOR = {3: [6, 2, 7, 3, 5, 4]}


def backfill_auction(db, auction: Auction) -> None:
    items = (
        db.query(AuctionItem)
        .filter(AuctionItem.auction_id == auction.id)
        .order_by(AuctionItem.order.asc())
        .all()
    )
    if not items:
        return
    total_slots = SESSION_ROSTER_SLOTS.get(auction.session, 0)
    filled: dict[int, int] = {}

    base_order, transition = ANCHORS.get(auction.id, (list(auction.nomination_order), len(items) + 1))
    order = list(base_order)

    for item in items:
        if item.order == transition and auction.id in POST_SWAP_ANCHOR:
            order = list(POST_SWAP_ANCHOR[auction.id])

        if item.nominated_by_user_id is None:
            idx = item.order % len(order)
            spots_remaining = total_slots - filled.get(order[idx], 0)
            if spots_remaining <= 0:
                for offset in range(1, len(order)):
                    j = (idx + offset) % len(order)
                    if total_slots - filled.get(order[j], 0) > 0:
                        order[idx], order[j] = order[j], order[idx]
                        break
            item.nominated_by_user_id = order[idx]

        if item.winning_user_id is not None:
            filled[item.winning_user_id] = filled.get(item.winning_user_id, 0) + 1

    print(f"  auction {auction.id} ({auction.session}): replay ends with order {order}")
    print(f"  auction {auction.id} ({auction.session}): actual stored order {auction.nomination_order}")


def run() -> None:
    db = SessionLocal()
    try:
        for auction in db.query(Auction).all():
            backfill_auction(db, auction)
        db.commit()
        print("Backfill committed.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
