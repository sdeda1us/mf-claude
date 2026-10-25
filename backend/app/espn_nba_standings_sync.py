"""Syncs NBA win/loss records directly from ESPN's standings API, run
from this backend process rather than depending on the scheduled Claude
Code routine's data/daily-sync/latest.json commit -- same reasoning as
nhl_standings_sync.py / espn_epl_standings_sync.py. Confirmed worth doing
the same way for NBA: the routine's 2026-10-25 batch had zero NBA entries
at all (not even a partial miss like EPL's Tottenham gap), leaving every
rostered NBA owner's point change stuck on "pending" despite the games
themselves already displaying correctly via espn_results_sync.py.

Unlike EPL's single table, ESPN splits NBA standings into two conference
children -- both get flattened into one 30-team batch; the fantasy score
formula (league_rules.compute_score) doesn't care about conference.

Run alongside daily_sync_pull.py's other pulls, from the same in-process
schedule (see daily_sync_pull_loop).

Can also be run on demand: `python -m app.espn_nba_standings_sync`
"""
import logging

import requests

from app.daily_score_sync import apply_daily_sync_batch
from app.database import SessionLocal
from app.schemas import DailySyncEntryIn
from app.team_name_aliases import canonicalize_team_name

logger = logging.getLogger("megafantasy.espn_nba_standings_sync")

STANDINGS_URL = "https://site.api.espn.com/apis/v2/sports/basketball/nba/standings"


def fetch_nba_standings() -> list[DailySyncEntryIn]:
    resp = requests.get(STANDINGS_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    resp.raise_for_status()
    payload = resp.json()

    entries = []
    for conference in payload["children"]:
        for entry in conference["standings"]["entries"]:
            name = canonicalize_team_name("NBA", entry["team"]["displayName"])
            stat_by_name = {s["name"]: s["value"] for s in entry["stats"] if "value" in s}
            stats = {
                "wins": int(stat_by_name["wins"]),
                "losses": int(stat_by_name["losses"]),
            }
            entries.append(DailySyncEntryIn(league="NBA", team=name, stats=stats))
    return entries


def sync_nba_standings() -> dict:
    entries = fetch_nba_standings()
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
    print(json.dumps(sync_nba_standings(), indent=2))
