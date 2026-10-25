"""Syncs URC table points/points difference directly from ESPN's
standings API -- same pattern as the other espn_*_standings_sync
modules, see espn_nba_standings_sync.py's docstring for why this
bypasses the routine.

Note the stat name trap: ESPN's rugby standings expose both
"differential" (a per-game average, e.g. 11.8) and "pointsDifference"
(the season-total aggregate league_rules.compute_score actually wants,
e.g. 47) -- confirmed by checking gamesPlayed * differential ≈
pointsDifference for a sample team. Easy to grab the wrong one since
"differential" sorts first alphabetically and reads as the obvious
match for "points_difference".

Only table_points/points_difference are synced -- the playoff bonus
fields (made_playoffs, won_quarterfinal, etc.) are left unset; the
2026-27 regular season runs well into spring, so there's nothing to get
wrong yet for those.

Run alongside daily_sync_pull.py's other pulls, from the same in-process
schedule (see daily_sync_pull_loop).

Can also be run on demand: `python -m app.espn_urc_standings_sync`
"""
import logging

from app.daily_score_sync import apply_daily_sync_batch
from app.database import SessionLocal
from app.espn_client import fetch_standings, flatten_standings_entries
from app.schemas import DailySyncEntryIn
from app.team_name_aliases import canonicalize_team_name

logger = logging.getLogger("megafantasy.espn_urc_standings_sync")


def fetch_urc_standings() -> list[DailySyncEntryIn]:
    raw = fetch_standings("URC")
    entries = []
    for entry in flatten_standings_entries(raw):
        name = canonicalize_team_name("URC", entry["team"]["displayName"])
        stat_by_name = {s["name"]: s["value"] for s in entry["stats"] if "value" in s}
        stats = {
            "table_points": int(stat_by_name["points"]),
            "points_difference": int(stat_by_name["pointsDifference"]),
        }
        entries.append(DailySyncEntryIn(league="URC", team=name, stats=stats))
    return entries


def sync_urc_standings() -> dict:
    entries = fetch_urc_standings()
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
    print(json.dumps(sync_urc_standings(), indent=2))
