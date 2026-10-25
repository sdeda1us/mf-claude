"""Syncs UCL league-phase points/goal-differential directly from ESPN's
standings API -- same pattern as the other espn_*_standings_sync
modules, see espn_nba_standings_sync.py's docstring for why this
bypasses the routine.

Only the league-phase base stats are synced -- the knockout-round bonus
fields (made_final_24, made_final_16, ..., won_final) are left unset.
The league phase itself runs through Jan 27, 2027, well before any
knockout round, so there's nothing to get wrong yet for those.

Run alongside daily_sync_pull.py's other pulls, from the same in-process
schedule (see daily_sync_pull_loop).

Can also be run on demand: `python -m app.espn_ucl_standings_sync`
"""
import logging

from app.daily_score_sync import apply_daily_sync_batch
from app.database import SessionLocal
from app.espn_client import fetch_standings, flatten_standings_entries
from app.schemas import DailySyncEntryIn
from app.team_name_aliases import canonicalize_team_name

logger = logging.getLogger("megafantasy.espn_ucl_standings_sync")


def fetch_ucl_standings() -> list[DailySyncEntryIn]:
    raw = fetch_standings("UCL")
    entries = []
    for entry in flatten_standings_entries(raw):
        name = canonicalize_team_name("UCL", entry["team"]["displayName"])
        stat_by_name = {s["name"]: s["value"] for s in entry["stats"] if "value" in s}
        stats = {
            "points": int(stat_by_name["points"]),
            "goal_differential": int(stat_by_name["pointDifferential"]),
        }
        entries.append(DailySyncEntryIn(league="UCL", team=name, stats=stats))
    return entries


def sync_ucl_standings() -> dict:
    entries = fetch_ucl_standings()
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
    print(json.dumps(sync_ucl_standings(), indent=2))
