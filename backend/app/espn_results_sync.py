"""Syncs yesterday's final scores for the Home page's "Yesterday's
Results" card directly from ESPN's scoreboard API, run from this backend
process rather than the scheduled Claude Code routine's
data/daily-results/ commit -- see espn_client.py's module docstring for
why (same reasoning as nhl_standings_sync.py). Run alongside
daily_sync_pull.py's other pulls, from the same in-process schedule (see
daily_sync_pull_loop).

Can also be run on demand: `python -m app.espn_results_sync`
"""
import logging
from datetime import timedelta

from app.daily_results_sync import sync_results_for_date
from app.daily_score_sync import today_eastern
from app.database import SessionLocal
from app.espn_client import LEAGUE_ENDPOINTS, extract_games, fetch_scoreboard
from app.schemas import DailyResultEntryIn
from app.team_name_aliases import canonicalize_team_name

logger = logging.getLogger("megafantasy.espn_results_sync")


def fetch_espn_results(result_date=None) -> list[DailyResultEntryIn]:
    result_date = result_date or (today_eastern() - timedelta(days=1))
    entries = []
    for league in LEAGUE_ENDPOINTS:
        try:
            raw = fetch_scoreboard(league, result_date)
        except Exception:
            logger.exception("ESPN results fetch failed for %s", league)
            continue
        for g in extract_games(raw):
            if g["home_score"] is None:
                continue  # not completed -- nothing to report
            entries.append(
                DailyResultEntryIn(
                    league=league,
                    home_team=canonicalize_team_name(league, g["home_team"]),
                    away_team=canonicalize_team_name(league, g["away_team"]),
                    home_score=g["home_score"],
                    away_score=g["away_score"],
                )
            )
    return entries


def sync_espn_results() -> dict:
    result_date = today_eastern() - timedelta(days=1)
    entries = fetch_espn_results(result_date)
    db = SessionLocal()
    try:
        result = sync_results_for_date(db, result_date, entries)
        db.commit()
    finally:
        db.close()
    return {"updated": result["updated"], "skipped": result["skipped"], "date": result_date.isoformat()}


if __name__ == "__main__":
    import json

    logging.basicConfig(level=logging.INFO)
    print(json.dumps(sync_espn_results(), indent=2))
