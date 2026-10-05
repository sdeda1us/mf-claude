"""Replaces the day's ScheduledGame rows for a set of leagues, so the
Home page's "Today's Games" widget can show matchups + venue + owning
player for the active season. Sourced the same way as
app/daily_score_sync.py -- a scheduled Claude Code cloud routine
web-searches today's schedule and commits data/daily-games/latest.json,
which app/daily_sync_pull.py pulls and feeds through sync_games_for_date
below.

Unlike sync_team_stats, an unmatched team name is NOT an error here --
a game with no matching Team row still displays (by its raw name, with
no owner), since showing "something is happening today" is more useful
than silently dropping the game. There's also no "only rostered teams"
filter the way apply_daily_sync_batch has for score entries -- games are
shown regardless of whether either side is drafted, so an undrafted
team's game still appears (with owner left blank).

Ingestion strategy: delete-then-reinsert per (league, game_date) rather
than upsert-by-matching -- simplest way to let the routine freely correct
yesterday's guess (postponements, venue changes) without needing stable
identity across runs. Does not commit -- caller owns the transaction,
same convention as apply_daily_sync_batch.

Run manually with:
    python -m app.daily_games_sync fixtures/games1.json
where the fixture is {"date": "YYYY-MM-DD", "games": [{"league",
"home_team", "away_team", "venue", "time_label"}, ...]}.
"""
from datetime import date

from app.models import ScheduledGame, Team
from app.schemas import DailyGameEntryIn


def sync_games_for_date(db, game_date: date, entries: list[DailyGameEntryIn]) -> int:
    """Deletes all existing ScheduledGame rows for game_date whose league
    appears in `entries`, then inserts one fresh row per entry. Returns
    the number of rows inserted."""
    leagues = {e.league for e in entries}
    if leagues:
        db.query(ScheduledGame).filter(
            ScheduledGame.game_date == game_date, ScheduledGame.league.in_(leagues)
        ).delete(synchronize_session=False)

    def _find_team_id(league: str, name: str) -> int | None:
        team = db.query(Team).filter(Team.league == league, Team.name == name).first()
        return team.id if team is not None else None

    count = 0
    for entry in entries:
        db.add(
            ScheduledGame(
                league=entry.league,
                game_date=game_date,
                home_team_id=_find_team_id(entry.league, entry.home_team),
                home_team_name=entry.home_team,
                away_team_id=_find_team_id(entry.league, entry.away_team),
                away_team_name=entry.away_team,
                venue=entry.venue,
                time_label=entry.time_label,
            )
        )
        count += 1
    db.flush()
    return count


if __name__ == "__main__":
    import json
    import sys
    from datetime import date as _date

    from app.database import SessionLocal

    if len(sys.argv) != 2:
        print("Usage: python -m app.daily_games_sync <fixture.json>")
        raise SystemExit(1)

    with open(sys.argv[1]) as f:
        payload = json.load(f)
    entries = [DailyGameEntryIn(**g) for g in payload.get("games", [])]
    game_date = _date.fromisoformat(payload["date"]) if payload.get("date") else _date.today()

    db = SessionLocal()
    try:
        n = sync_games_for_date(db, game_date, entries)
        db.commit()
        print(f"Synced {n} games for {game_date}")
    finally:
        db.close()
