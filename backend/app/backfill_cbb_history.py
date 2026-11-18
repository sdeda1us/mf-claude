"""One-off backfill: writes day-by-day NCAAMB/NCAAWB TeamDailyScore history
for every real game played since the 2026-27 season started (Nov 1, 2026),
instead of the single "whatever the record is today" snapshot the normal
daily sync produces for a team's first-ever row. Without this, the Score
Over Time chart and Yesterday's Scoring by Player table would show one
lump catch-up jump on whatever day CBB first gets synced, instead of each
real game's point change landing on its own day.

Reads a JSON file (default data/ncaamb-ncaawb-backfill.json at the repo
root) a cloud research routine produces, shaped:
    {"NCAAMB": [{"team": "Duke Blue Devils",
                 "games": [{"date": "2026-11-03", "result": "W"}, ...]},
                ...],
     "NCAAWB": [...]}
Games don't need to be pre-sorted -- this script sorts each team's games
chronologically itself before replaying them.

For each team, in chronological order, calls daily_score_sync.sync_team_stats
with an explicit as_of_date for every date a game happened, accumulating
wins/losses as it goes. Same "day after" dating convention every other
league's sync already uses (see daily_score_sync.py's module docstring and
routers/seasons.py's _team_point_change) -- a game played on date D is
stamped with as_of_date D+1, so a Nov 3 game shows up as Nov 4's point
gain, consistent with how every other league's rows are interpreted.

Tournament/seed flags (reg_season_conf_champ, conf_tourney_champ,
ncaa_qualifier, seed_1, seed_2, won_round_of_64, won_round_of_32,
won_sweet_16, won_elite_8, won_final_4, won_championship) are kept False
for every row -- conference tournaments run in March, long after any date
this backfill covers.

Safe to re-run: sync_team_stats upserts both TeamSeasonResult (in place)
and the TeamDailyScore row for a given as_of_date (idempotent per
team+date), so re-running with the same input just overwrites with the
same numbers.

Run with: python -m app.backfill_cbb_history [path-to-json]
(or `railway ssh -- python -m app.backfill_cbb_history` in production)
"""
import json
import sys
from datetime import date, timedelta
from pathlib import Path

from app.daily_score_sync import SeasonNotStartedError, TeamNotFoundError, sync_team_stats
from app.database import SessionLocal

DEFAULT_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "ncaamb-ncaawb-backfill.json"

ZERO_FLAGS = {
    "reg_season_conf_champ": False,
    "conf_tourney_champ": False,
    "ncaa_qualifier": False,
    "seed_1": False,
    "seed_2": False,
    "won_round_of_64": False,
    "won_round_of_32": False,
    "won_sweet_16": False,
    "won_elite_8": False,
    "won_final_4": False,
    "won_championship": False,
}


def run(path: Path = DEFAULT_PATH) -> None:
    payload = json.loads(path.read_text())
    db = SessionLocal()
    synced = 0
    skipped: list[str] = []
    try:
        for league in ("NCAAMB", "NCAAWB"):
            for team_entry in payload.get(league, []):
                team_name = team_entry["team"]
                games = sorted(team_entry.get("games", []), key=lambda g: g["date"])
                wins = losses = 0
                for g in games:
                    if g["result"] == "W":
                        wins += 1
                    elif g["result"] == "L":
                        losses += 1
                    else:
                        skipped.append(
                            f"{league} {team_name}: unrecognized result {g['result']!r} on {g['date']}"
                        )
                        continue
                    game_date = date.fromisoformat(g["date"])
                    as_of = game_date + timedelta(days=1)
                    stats = {"wins": wins, "losses": losses, **ZERO_FLAGS}
                    try:
                        sync_team_stats(db, league, team_name, stats, as_of_date=as_of)
                        synced += 1
                    except (TeamNotFoundError, SeasonNotStartedError) as e:
                        skipped.append(f"{league} {team_name} {g['date']}: {e}")
        db.commit()
    finally:
        db.close()
    print(f"Synced {synced} day-rows.")
    if skipped:
        print(f"Skipped {len(skipped)}:")
        for s in skipped:
            print(" -", s)


if __name__ == "__main__":
    run(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH)
