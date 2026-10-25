"""Syncs EPL standings (points + goal differential -- the two stats
league_rules.compute_score's EPL formula needs) directly from ESPN's
standings API, run from this backend process rather than depending on
the scheduled Claude Code routine's data/daily-sync/latest.json commit
-- same reasoning as nhl_standings_sync.py bypassing the routine for NHL
standings. Confirmed worth doing the same way for EPL: the routine's
2026-10-25 batch had a row for Chelsea but none for Tottenham Hotspur,
the same kind of per-day coverage gap found in the old games/results
pipeline, which showed up as a stuck "pending" point-change for
Tottenham's owner on the Home page despite the match itself (Chelsea
0-2 Tottenham) already displaying correctly via espn_results_sync.py.

One ESPN call returns the full 20-team table, so there's no partial-
coverage risk here the way there was with 7 separate scoreboard calls.

Run alongside daily_sync_pull.py's other pulls, from the same in-process
schedule (see daily_sync_pull_loop).

Can also be run on demand: `python -m app.espn_epl_standings_sync`
"""
import logging

import requests

from app.daily_score_sync import apply_daily_sync_batch
from app.database import SessionLocal
from app.schemas import DailySyncEntryIn
from app.team_name_aliases import canonicalize_team_name

logger = logging.getLogger("megafantasy.espn_epl_standings_sync")

STANDINGS_URL = "https://site.api.espn.com/apis/v2/sports/soccer/eng.1/standings"


def fetch_epl_standings() -> list[DailySyncEntryIn]:
    resp = requests.get(STANDINGS_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    resp.raise_for_status()
    payload = resp.json()

    entries = []
    for entry in payload["children"][0]["standings"]["entries"]:
        name = canonicalize_team_name("EPL", entry["team"]["displayName"])
        # "overall" (e.g. "7-0-1") has no "value" key, unlike every
        # numeric stat -- skip entries without one rather than crash.
        stat_by_name = {s["name"]: s["value"] for s in entry["stats"] if "value" in s}
        stats = {
            "standings_points": int(stat_by_name["points"]),
            "goal_differential": int(stat_by_name["pointDifferential"]),
        }
        entries.append(DailySyncEntryIn(league="EPL", team=name, stats=stats))
    return entries


def sync_epl_standings() -> dict:
    entries = fetch_epl_standings()
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
    print(json.dumps(sync_epl_standings(), indent=2))
