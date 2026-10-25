"""Syncs today's schedule for the Home page's "Today's Games" widget
directly from ESPN's scoreboard API, run from this backend process
rather than the scheduled Claude Code routine's data/daily-games/
commit -- see espn_client.py's module docstring for why (same reasoning
as nhl_standings_sync.py). Run alongside daily_sync_pull.py's other
pulls, from the same in-process schedule (see daily_sync_pull_loop).

Can also be run on demand: `python -m app.espn_games_sync`
"""
import logging

from app.daily_games_sync import sync_games_for_date
from app.daily_score_sync import today_eastern
from app.database import SessionLocal
from app.espn_client import LEAGUE_ENDPOINTS, extract_games, fetch_scoreboard
from app.schemas import DailyGameEntryIn
from app.team_name_aliases import canonicalize_team_name

logger = logging.getLogger("megafantasy.espn_games_sync")


def fetch_espn_games(game_date=None) -> list[DailyGameEntryIn]:
    game_date = game_date or today_eastern()
    entries = []
    for league in LEAGUE_ENDPOINTS:
        try:
            raw = fetch_scoreboard(league, game_date)
        except Exception:
            logger.exception("ESPN games fetch failed for %s", league)
            continue
        for g in extract_games(raw):
            entries.append(
                DailyGameEntryIn(
                    league=league,
                    home_team=canonicalize_team_name(league, g["home_team"]),
                    away_team=canonicalize_team_name(league, g["away_team"]),
                    venue=g["venue"],
                    time_label=g["time_label"],
                )
            )
    return entries


def sync_espn_games() -> dict:
    game_date = today_eastern()
    entries = fetch_espn_games(game_date)
    db = SessionLocal()
    try:
        count = sync_games_for_date(db, game_date, entries)
        db.commit()
    finally:
        db.close()
    return {"synced": count, "date": game_date.isoformat()}


if __name__ == "__main__":
    import json

    logging.basicConfig(level=logging.INFO)
    print(json.dumps(sync_espn_games(), indent=2))
