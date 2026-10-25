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
from datetime import date, timedelta

from app.models import ScheduledGame
from app.schemas import DailyResultEntryIn
from app.season_labels import SEASON_START_DATE
from app.team_name_aliases import canonicalize_team_name

# How far back to look for an unresolved (home_score IS NULL) ScheduledGame
# row when a result's exact (game_date, league, home_team, away_team)
# tuple has no match. Covers a fixture whose games-sync guessed the wrong
# date -- a rescheduled kickoff (e.g. the Premier League bumping a match
# to a different day for TV) or a postponement -- which otherwise never
# gets its result attached: the schedule row sits under the wrong date
# forever, and the correctly-dated result has nothing to match against.
# A week comfortably covers any such slip without reaching back far enough
# to risk matching an unrelated earlier fixture between the same two teams.
RESULT_MATCH_LOOKBACK_DAYS = 7


def sync_results_for_date(db, game_date: date, entries: list[DailyResultEntryIn]) -> dict:
    """Updates home_score/away_score on each matching ScheduledGame row.
    Returns {"updated": int, "skipped": [{"league", "home_team",
    "away_team"}, ...]} for rows with no schedule match. Does not commit
    -- caller owns the transaction.

    An entry for a league whose real-world regular season hadn't started
    yet as of game_date (SEASON_START_DATE) is a preseason/exhibition
    result -- skipped the same as an unmatched game, since it shouldn't
    appear on "Yesterday's Results" or count toward fantasy scoring. In
    practice sync_games_for_date already keeps these out of the schedule,
    so this mostly guards against a result reported with no matching
    games-sync entry.

    A result with no EXACT (game_date, league, teams) match falls back to
    the most recent still-unresolved ScheduledGame for that league/team
    pair within RESULT_MATCH_LOOKBACK_DAYS, and corrects its game_date to
    game_date -- see RESULT_MATCH_LOOKBACK_DAYS above for why. Only a
    truly orphaned result (no schedule row at all, under any recent date)
    is skipped."""
    updated = 0
    skipped: list[dict] = []
    for entry in entries:
        if game_date < SEASON_START_DATE.get(entry.league, date.min):
            skipped.append(
                {"league": entry.league, "home_team": entry.home_team, "away_team": entry.away_team}
            )
            continue
        home_team = canonicalize_team_name(entry.league, entry.home_team)
        away_team = canonicalize_team_name(entry.league, entry.away_team)
        game = (
            db.query(ScheduledGame)
            .filter(
                ScheduledGame.game_date == game_date,
                ScheduledGame.league == entry.league,
                ScheduledGame.home_team_name == home_team,
                ScheduledGame.away_team_name == away_team,
            )
            .first()
        )
        if game is None:
            game = (
                db.query(ScheduledGame)
                .filter(
                    ScheduledGame.game_date >= game_date - timedelta(days=RESULT_MATCH_LOOKBACK_DAYS),
                    ScheduledGame.game_date < game_date,
                    ScheduledGame.league == entry.league,
                    ScheduledGame.home_team_name == home_team,
                    ScheduledGame.away_team_name == away_team,
                    ScheduledGame.home_score.is_(None),
                )
                .order_by(ScheduledGame.game_date.desc())
                .first()
            )
            if game is not None:
                game.game_date = game_date
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
