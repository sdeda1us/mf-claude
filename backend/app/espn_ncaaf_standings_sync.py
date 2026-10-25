"""Syncs NCAAF win/loss records directly from ESPN's standings API --
same pattern as the other espn_*_standings_sync modules, see
espn_nba_standings_sync.py's docstring for why this bypasses the
routine.

ESPN's overall-record stats for this endpoint are oddly incomplete: each
team's "stats" list has a "wins" entry but no matching overall "losses"
entry (only a conference-scoped "divisionLosses", not what
league_rules.compute_score needs) -- confirmed by inspecting a sample
team's raw stat list, not a guess. The one stat that DOES carry the true
overall record is "total", whose value is always null but whose
"summary" field is a plain "W-L" string (e.g. "7-1") -- so losses is
parsed from there instead of read directly like every other league here.

Only wins/reg_season_losses are synced -- playoff_bid/playoff_wins/
playoff_bye are left unset, same intentional limitation the other
espn_*_standings_sync modules have for their leagues' playoffs: the CFP
is a few weeks off from "today," so there's nothing to get wrong yet.

Run alongside daily_sync_pull.py's other pulls, from the same in-process
schedule (see daily_sync_pull_loop).

Can also be run on demand: `python -m app.espn_ncaaf_standings_sync`
"""
import logging

from app.daily_score_sync import apply_daily_sync_batch
from app.database import SessionLocal
from app.espn_client import fetch_standings, flatten_standings_entries
from app.schemas import DailySyncEntryIn
from app.team_name_aliases import canonicalize_team_name

logger = logging.getLogger("megafantasy.espn_ncaaf_standings_sync")


def fetch_ncaaf_standings() -> list[DailySyncEntryIn]:
    raw = fetch_standings("NCAAF")
    entries = []
    for entry in flatten_standings_entries(raw):
        name = canonicalize_team_name("NCAAF", entry["team"]["displayName"])
        total = next(s for s in entry["stats"] if s.get("type") == "total")
        wins, losses = (int(n) for n in total["summary"].split("-")[:2])
        stats = {"wins": wins, "reg_season_losses": losses}
        entries.append(DailySyncEntryIn(league="NCAAF", team=name, stats=stats))
    return entries


def sync_ncaaf_standings() -> dict:
    entries = fetch_ncaaf_standings()
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
    print(json.dumps(sync_ncaaf_standings(), indent=2))
