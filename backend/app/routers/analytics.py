from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.league_rules import LEAGUE_SESSION
from app.models import Auction, AuctionStatus, RosterEntry, Season, Team, User
from app.schemas import AuctionSpendingFacetOut, AuctionSpendingOut, AuctionSummaryOut

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/auctions", response_model=list[AuctionSummaryOut])
def list_auctions(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    """Every auction across every season, for the analytics page's picker.
    Ordered so the default (first) entry is always the most useful one to
    land on: any still-in-progress auction (pending/live) outranks every
    complete one regardless of age, and ties within each group break by
    newest-created first."""
    rows = (
        db.query(Auction, Season.name)
        .join(Season, Auction.season_id == Season.id)
        .order_by((Auction.status == AuctionStatus.complete).asc(), Auction.created_at.desc())
        .all()
    )
    return [
        AuctionSummaryOut(
            id=a.id,
            season_id=a.season_id,
            season_name=season_name,
            session=a.session,
            status=a.status,
            created_at=a.created_at,
        )
        for a, season_name in rows
    ]


@router.get("/auctions/{auction_id}/spending", response_model=AuctionSpendingOut)
def auction_spending(
    auction_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    """Average $ spent per team, broken down by real-world league, for
    this one auction (season+session) -- one facet for every owner plus a
    combined "whole league" facet, each with the same set of league
    categories so the radial charts on the analytics page stay directly
    comparable across facets."""
    auction = db.get(Auction, auction_id)
    if auction is None:
        raise HTTPException(status_code=404, detail="Auction not found")
    season = db.get(Season, auction.season_id)

    leagues = sorted(lg for lg, session in LEAGUE_SESSION.items() if session == auction.session)

    entries = (
        db.query(RosterEntry)
        .join(Team, RosterEntry.team_id == Team.id)
        .filter(RosterEntry.season_id == auction.season_id, Team.league.in_(leagues))
        .all()
    )

    # (owner_id | None for "whole league") -> league -> [prices]
    prices: dict[int | None, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for entry in entries:
        price = float(entry.price_paid)
        prices[entry.user_id][entry.team.league].append(price)
        prices[None][entry.team.league].append(price)

    def facet_for(owner_id: int | None, display_name: str) -> AuctionSpendingFacetOut:
        by_owner = prices.get(owner_id, {})
        by_league = {}
        for lg in leagues:
            vals = by_owner.get(lg, [])
            by_league[lg] = sum(vals) / len(vals) if vals else 0.0
        teams_sold = sum(len(v) for v in by_owner.values())
        return AuctionSpendingFacetOut(
            owner_id=owner_id, display_name=display_name, teams_sold=teams_sold, by_league=by_league
        )

    facets = [facet_for(None, "Whole League")]
    owner_ids = auction.nomination_order or sorted({e.user_id for e in entries})
    users_by_id = {u.id: u for u in db.query(User).filter(User.id.in_(owner_ids)).all()}
    for uid in owner_ids:
        user = users_by_id.get(uid)
        facets.append(facet_for(uid, user.display_name if user else f"User #{uid}"))

    return AuctionSpendingOut(
        auction_id=auction.id,
        season_name=season.name if season else "",
        session=auction.session,
        leagues=leagues,
        facets=facets,
    )
