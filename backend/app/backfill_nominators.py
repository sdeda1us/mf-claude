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
historical item would misattribute anything nominated before a later
swap.

Instead, for each auction this replays the exact same skip_full_players_turn
algorithm forward, item by item, starting from a known-good anchor (the
order as it stood right when the item at that anchor's item order was
about to be nominated), tracking each user's filled-spot count as it goes.

The one real anchor needed: auction id 3 (fall, season 2) is this app's
only auction where a swap has ever actually fired. I manually ran
skip_full_players_turn against it on 2026-10-03, at a moment captured
mid-conversation: nomination_order became [6, 2, 7, 3, 5, 4] with exactly
229 items already sold. Items 0-228 were all created before the skip-logic
existed at all, so they can't have been swapped -- the plain formula with
the PRE-swap order [6, 3, 7, 2, 5, 4] is correct for those.

The filled-spot count at that same anchor point can't be reconstructed
purely by replaying AuctionItem winners from order 0 -- two manual
roster corrections (a RosterEntry added for one user, another deleted for
another, both made in the same conversation turn as the manual swap, i.e.
at essentially this exact anchor point) aren't tied to any AuctionItem at
all. So instead of replaying from zero, the filled count at the anchor is
derived backwards from each user's REAL, current roster_status_by_user
spots_filled, minus whatever items 229+ will themselves re-contribute as
the replay below processes them -- which nets out to the correct
as-of-the-anchor count regardless of those two untracked manual edits.
"""

from app.auction_service import roster_status_by_user
from app.database import SessionLocal
from app.league_rules import LEAGUE_SESSION, ROSTER_LIMITS
from app.models import Auction, AuctionItem, Season

SESSION_ROSTER_SLOTS = {
    session: sum(limit for league, limit in ROSTER_LIMITS.items() if LEAGUE_SESSION.get(league) == session)
    for session in ("fall", "spring")
}

# auction_id -> (pre_swap_order, anchor_item_order, post_swap_order).
# Items before anchor_item_order use pre_swap_order via the plain formula
# (no fullness tracking needed -- nothing could have swapped them yet).
# Items from anchor_item_order onward are replayed forward starting from
# post_swap_order, with filled-spot counts seeded as described above.
ANCHORS: dict[int, tuple[list[int], int, list[int]]] = {
    3: ([6, 3, 7, 2, 5, 4], 229, [6, 2, 7, 3, 5, 4]),
}


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

    anchor = ANCHORS.get(auction.id)
    if anchor is None:
        # No swap has ever fired for this auction -- the current order is
        # still the original one, and nobody's ever been full mid-replay,
        # so a plain zero-seeded replay from item 0 is exact (verified by
        # dry run: matches the real stored order for auctions 1 and 2).
        order = list(auction.nomination_order)
        filled: dict[int, int] = {}
        replay_items = items
    else:
        pre_swap_order, transition, post_swap_order = anchor
        for item in items:
            if item.order >= transition:
                break
            if item.nominated_by_user_id is None:
                item.nominated_by_user_id = pre_swap_order[item.order % len(pre_swap_order)]

        season = db.get(Season, auction.season_id)
        real_filled = {
            uid: status.spots_filled
            for uid, status in roster_status_by_user(db, season, auction.session).items()
        }
        replay_items = [i for i in items if i.order >= transition]
        contributed_in_window: dict[int, int] = {}
        for item in replay_items:
            if item.winning_user_id is not None:
                contributed_in_window[item.winning_user_id] = (
                    contributed_in_window.get(item.winning_user_id, 0) + 1
                )
        filled = {
            uid: real_filled.get(uid, 0) - contributed_in_window.get(uid, 0)
            for uid in real_filled
        }
        order = list(post_swap_order)

    for item in replay_items:
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
