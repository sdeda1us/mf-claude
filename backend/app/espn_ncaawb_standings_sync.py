"""Syncs NCAAWB (women's college basketball) win-loss records directly
from ESPN's standings API -- see espn_ncaamb_standings_sync.py's
docstring for the full reasoning (identical shape/pitfalls on the
women's endpoint: overall record is the first "wins"/"losses" block,
followed by Home/Road/ranked-opponent splits that a naive
{s["name"]: s["value"]} comprehension would silently prefer instead).

Only wins/losses are synced -- conference-tournament/NCAA-tournament
bonus fields are left unset, same reasoning as the men's sync.

Run alongside daily_sync_pull.py's other pulls, from the same in-process
schedule (see daily_sync_pull_loop).

Can also be run on demand: `python -m app.espn_ncaawb_standings_sync`
"""
import logging

from app.daily_score_sync import apply_daily_sync_batch
from app.database import SessionLocal
from app.espn_client import flatten_standings_entries, fetch_standings
from app.espn_ncaamb_standings_sync import _first_stat
from app.schemas import DailySyncEntryIn
from app.team_name_aliases import canonicalize_team_name

logger = logging.getLogger("megafantasy.espn_ncaawb_standings_sync")

LEAGUE = "NCAAWB"


def fetch_ncaawb_standings() -> list[DailySyncEntryIn]:
    raw = fetch_standings(LEAGUE)
    entries = []
    for entry in flatten_standings_entries(raw):
        stats = entry["stats"]
        wins = _first_stat(stats, "wins")
        losses = _first_stat(stats, "losses")
        if wins is None or losses is None:
            continue
        name = canonicalize_team_name(LEAGUE, entry["team"]["displayName"])
        entries.append(
            DailySyncEntryIn(league=LEAGUE, team=name, stats={"wins": int(wins), "losses": int(losses)})
        )
    return entries


def sync_ncaawb_standings() -> dict:
    entries = fetch_ncaawb_standings()
    db = SessionLocal()
    try:
        result = apply_daily_sync_batch(db, entries)
        db.commit()
    finally:
        db.close()
    return {"synced": result.synced, "skipped": [s.model_dump() for s in result.skipped]}


if __name__ == "__main__":
    import json

    logging.basicConfig(level=logging.INFO)
    print(json.dumps(sync_ncaawb_standings(), indent=2))
