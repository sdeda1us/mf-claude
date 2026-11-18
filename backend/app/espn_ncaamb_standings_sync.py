"""Syncs NCAAMB (men's college basketball) win-loss records directly
from ESPN's standings API -- same pattern as the other
espn_*_standings_sync modules, see espn_nba_standings_sync.py's
docstring for why this bypasses the routine. Added once the daily
cloud routine proved unreliable for this league specifically: 84
rostered NCAAMB/NCAAWB teams is more research than its WebSearch-budget
-limited runs could reliably finish in one pass (see
app/backfill_cbb_history.py's module docstring for the one-off
historical backfill this complements going forward).

ESPN's standings entries are NOT one clean stat block per team the way
NFL/EPL/UCL/URC's are -- ESPN concatenates the team's overall record's
13 stat fields, then a same-shaped "Home" split, "Road" split, "vs AP
Top 25" split, etc., each block ending in a trailing marker entry (name
= that split's label, e.g. "overall"/"Home"/"Road", value absent,
displayValue like "4-1") rather than being tagged up front. A naive
{s["name"]: s["value"] for s in stats} dict comprehension (as
espn_ucl_standings_sync.py uses, safe there since UCL has no splits)
would silently keep the LAST "wins"/"losses" it sees -- usually the
smallest, most-zero split (conference or ranked-opponent record this
early in the season) -- instead of the real overall record. The
overall record is always the FIRST block, so _first_stat below takes
the first matching "name", not the last.

Only wins/losses are synced -- conference-tournament/NCAA-tournament
bonus fields (reg_season_conf_champ, conf_tourney_champ, ncaa_qualifier,
seed_1, seed_2, won_round_of_64, won_round_of_32, won_sweet_16,
won_elite_8, won_final_4, won_championship) are left unset, same
"nothing to get wrong yet" reasoning as NFL/UCL's own synced-field
subsets -- conference tournaments run in March, long before this needs
revisiting.

Run alongside daily_sync_pull.py's other pulls, from the same in-process
schedule (see daily_sync_pull_loop).

Can also be run on demand: `python -m app.espn_ncaamb_standings_sync`
"""
import logging

from app.daily_score_sync import apply_daily_sync_batch
from app.database import SessionLocal
from app.espn_client import flatten_standings_entries, fetch_standings
from app.schemas import DailySyncEntryIn
from app.team_name_aliases import canonicalize_team_name

logger = logging.getLogger("megafantasy.espn_ncaamb_standings_sync")

LEAGUE = "NCAAMB"


def _first_stat(stats: list[dict], name: str) -> float | None:
    for s in stats:
        if s.get("name") == name and "value" in s:
            return s["value"]
    return None


def fetch_ncaamb_standings() -> list[DailySyncEntryIn]:
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


def sync_ncaamb_standings() -> dict:
    entries = fetch_ncaamb_standings()
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
    print(json.dumps(sync_ncaamb_standings(), indent=2))
