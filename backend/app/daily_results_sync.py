"""Fills in home_score/away_score on existing ScheduledGame rows for a
past date, so the Home page's "Yesterday's Results" card has something
to show. Sourced the same way as app/daily_games_sync.py -- the scheduled
Claude Code routine reads the schedule it already committed the day
before (before overwriting it with today's), looks up each game's final
score, and commits data/daily-results/latest.json, which
app/daily_sync_pull.py pulls and feeds through sync_results_for_date
below.

Unlike sync_games_for_date, this is an in-place UPDATE, not a
delete-then-reinsert -- the schedule row already exists (from the
previous day's games-sync) and only needs its score filled in. A result
with no matching ScheduledGame row (team names/date didn't line up with
what was scheduled) is skipped, not inserted -- there would be no owner
information to attach to a schedule-less row anyway.

Run manually with:
    python -m app.daily_results_sync fixtures/results1.json
where the fixture is {"date": "YYYY-MM-DD", "results": [{"league",
"home_team", "away_team", "home_score", "away_score"}, ...]}.
"""
from datetime import date

from app.models import ScheduledGame
from app.schemas import DailyResultEntryIn


def sync_results_for_date(db, game_date: date, entries: list[DailyResultEntryIn]) -> dict:
    """Updates home_score/away_score on each matching ScheduledGame row.
    Returns {"updated": int, "skipped": [{"league", "home_team",
    "away_team"}, ...]} for rows with no schedule match. Does not commit
    -- caller owns the transaction."""
    updated = 0
    skipped: list[dict] = []
    for entry in entries:
        game = (
            db.query(ScheduledGame)
            .filter(
                ScheduledGame.game_date == game_date,
                ScheduledGame.league == entry.league,
                ScheduledGame.home_team_name == entry.home_team,
                ScheduledGame.away_team_name == entry.away_team,
            )
            .first()
        )
        if game is None:
            skipped.append(
                {"league": entry.league, "home_team": entry.home_team, "away_team": entry.away_team}
            )
            continue
        game.home_score = entry.home_score
        game.away_score = entry.away_score
        updated += 1
    db.flush()
    return {"updated": updated, "skipped": skipped}


if __name__ == "__main__":
    import json
    import sys
    from datetime import date as _date

    from app.database import SessionLocal

    if len(sys.argv) != 2:
        print("Usage: python -m app.daily_results_sync <fixture.json>")
        raise SystemExit(1)

    with open(sys.argv[1]) as f:
        payload = json.load(f)
    entries = [DailyResultEntryIn(**r) for r in payload.get("results", [])]
    game_date = _date.fromisoformat(payload["date"]) if payload.get("date") else _date.today()

    db = SessionLocal()
    try:
        result = sync_results_for_date(db, game_date, entries)
        db.commit()
        print(f"Updated {result['updated']} game(s) for {game_date}")
        for s in result["skipped"]:
            print(f"  SKIPPED (no schedule match): {s}")
    finally:
        db.close()
