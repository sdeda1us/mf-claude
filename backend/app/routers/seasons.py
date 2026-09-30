from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_commissioner, get_current_user
from app.league_rules import compute_score
from app.models import (
    Auction,
    AuctionItem,
    Bid,
    QueueEntry,
    ReserveBid,
    RosterEntry,
    Season,
    SeasonStatus,
    Team,
    TeamSeasonResult,
    User,
)
from app.schemas import ScoringSummaryOut, ScoringSummaryOwnerOut, SeasonCreateIn, SeasonOut

router = APIRouter(prefix="/seasons", tags=["seasons"])

# The only two leagues every team in the pool has actually been drafted
# for so far -- a per-owner scoring summary is only meaningful once
# nobody's missing from the picture. Extend this list by hand as other
# leagues finish their own auctions; not worth auto-detecting "fully
# drafted" for what's currently just two leagues.
SCORING_SUMMARY_LEAGUES = ["EPL", "URC"]


@router.get("", response_model=list[SeasonOut])
def list_seasons(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Season).order_by(Season.created_at.desc()).all()


@router.get("/{season_id}/scoring-summary", response_model=ScoringSummaryOut)
def scoring_summary(
    season_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)
):
    """Per-owner points for the leagues in SCORING_SUMMARY_LEAGUES, from
    each drafted team's most recent TeamSeasonResult (whichever
    season_label sorts latest, per team -- see results_by_team below).
    For EPL/URC that's the current, in-progress 2026-27 season, kept
    current by re-running app/update_live_standings.py against a fresh
    table lookup (there's no live sports-data feed wired into this app,
    so nothing updates these rows on its own). A team with no
    TeamSeasonResult row at all (e.g. newly promoted into a league, with
    no row yet under its new league) silently contributes 0 rather than
    erroring, same spirit as /leagues/example-scores."""
    if db.get(Season, season_id) is None:
        raise HTTPException(status_code=404, detail="Season not found")

    entries = (
        db.query(RosterEntry)
        .join(Team, RosterEntry.team_id == Team.id)
        .filter(RosterEntry.season_id == season_id, Team.league.in_(SCORING_SUMMARY_LEAGUES))
        .all()
    )
    # Ordered oldest-label-first so that when a team has more than one
    # season's row (e.g. "2025-26" and "2026-27"), the later one wins this
    # dict's last-write-wins overwrite -- season labels sort chronologically
    # as plain strings ("2026-27" > "2025-26"), so no separate date field
    # is needed to know which is newer.
    results_by_team = {
        r.team_id: r
        for r in db.query(TeamSeasonResult)
        .filter(TeamSeasonResult.league.in_(SCORING_SUMMARY_LEAGUES))
        .order_by(TeamSeasonResult.season_label.asc())
    }

    season_label_by_league: dict[str, str] = {}
    totals: dict[int, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for entry in entries:
        result = results_by_team.get(entry.team_id)
        if result is None:
            continue
        league = entry.team.league
        season_label_by_league.setdefault(league, result.season_label)
        totals[entry.user_id][league] += compute_score(league, result.stats)

    owners = [
        ScoringSummaryOwnerOut(
            user_id=u.id,
            display_name=u.display_name,
            by_league={lg: totals[u.id].get(lg, 0.0) for lg in SCORING_SUMMARY_LEAGUES},
            total=sum(totals[u.id].values()),
        )
        for u in db.query(User).all()
    ]
    owners.sort(key=lambda o: o.total, reverse=True)

    return ScoringSummaryOut(
        leagues=SCORING_SUMMARY_LEAGUES,
        season_label_by_league=season_label_by_league,
        owners=owners,
    )


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
