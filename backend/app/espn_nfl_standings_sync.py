"""Syncs NFL win/loss/tie records directly from ESPN's standings API --
same pattern as espn_nba_standings_sync.py / espn_epl_standings_sync.py,
see those modules' docstrings for why this bypasses the routine.

Only wins/ties/losses are synced -- playoff bonus fields
(won_round1_or_bye, won_conf_champ, etc.) are left unset, same
intentional limitation nhl_standings_sync.py already has for the Stanley
Cup playoffs: the NFL playoffs are months away (Feb 2027), so there's
nothing to get wrong yet, and wiring up playoff-bonus detection from
ESPN is a separate problem for closer to that date.

Run alongside daily_sync_pull.py's other pulls, from the same in-process
schedule (see daily_sync_pull_loop).

Can also be run on demand: `python -m app.espn_nfl_standings_sync`
"""
import logging

from app.daily_score_sync import apply_daily_sync_batch
from app.database import SessionLocal
from app.espn_client import fetch_standings, flatten_standings_entries
from app.schemas import DailySyncEntryIn
from app.team_name_aliases import canonicalize_team_name

logger = logging.getLogger("megafantasy.espn_nfl_standings_sync")


def fetch_nfl_standings() -> list[DailySyncEntryIn]:
    raw = fetch_standings("NFL")
    entries = []
    for entry in flatten_standings_entries(raw):
        name = canonicalize_team_name("NFL", entry["team"]["displayName"])
        stat_by_name = {s["name"]: s["value"] for s in entry["stats"] if "value" in s}
        stats = {
            "wins": int(stat_by_name["wins"]),
            "ties": int(stat_by_name.get("ties", 0)),
        }
        entries.append(DailySyncEntryIn(league="NFL", team=name, stats=stats))
    return entries


def sync_nfl_standings() -> dict:
    entries = fetch_nfl_standings()
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
    print(json.dumps(sync_nfl_standings(), indent=2))
