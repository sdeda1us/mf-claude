"""Records one TeamDailyScore row per rostered team per real-world day, so
score changes can be tracked day-over-day instead of only ever seeing the
latest cumulative total (TeamSeasonResult, which this still keeps updated
in place exactly as before -- nothing that reads it needs to change).

Meant to be fed by an external lookup, since there's no live sports-data
feed wired into this app -- in practice, a Claude Code scheduled cloud
routine that web-searches current standings once a day and POSTs the
result to POST /api/scoring-sync/batch (see routers/scoring_sync.py),
which calls sync_team_stats below for each rostered team. This module's
own __main__ entry point is for local/manual test runs against a JSON
fixture rather than the real daily path.

First-ever-row backdating: when this is called for a (team, season_label)
that has no TeamDailyScore row yet, the new row is dated *yesterday*
rather than today, regardless of how much of the real season has already
been played. This is deliberate -- most leagues already have games
played by the time this fall's auction finishes, so whatever cumulative
stats already exist get attributed to one "yesterday" snapshot rather
than fabricating day-by-day history that was never actually tracked; real
deltas only start accruing from the next sync forward. Every later sync
for that same team+season uses the real current date instead.

Run manually with:
    python -m app.daily_score_sync fixtures/day1.json
where the fixture is a JSON list of {"league", "team", "stats"} objects.
"""
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from app.database import SessionLocal
from app.league_rules import compute_score
from app.models import Team, TeamDailyScore, TeamSeasonResult
from app.season_labels import CURRENT_SEASON

EASTERN = ZoneInfo("America/New_York")  # matches backup.py / quiet_hours.py


class TeamNotFoundError(Exception):
    pass


class UnsupportedLeagueError(Exception):
    pass


def today_eastern() -> date:
    return datetime.now(EASTERN).date()


def sync_team_stats(
    db,
    league: str,
    team_name: str,
    stats: dict,
    as_of_date: date | None = None,
) -> TeamDailyScore:
    """Upsert TeamSeasonResult (unchanged overwrite-in-place behavior) and
    append/update one TeamDailyScore row for today (or `as_of_date`, when
    explicitly passed for a backfill/test run -- the first-ever-row
    backdating rule only applies when as_of_date is left as None, i.e. the
    normal daily-sync path)."""
    if league not in CURRENT_SEASON:
        raise UnsupportedLeagueError(league)
    team = db.query(Team).filter(Team.league == league, Team.name == team_name).first()
    if team is None:
        raise TeamNotFoundError(f"{league} {team_name}")
    season_label = CURRENT_SEASON[league]

    existing_season_result = (
        db.query(TeamSeasonResult)
        .filter(TeamSeasonResult.team_id == team.id, TeamSeasonResult.season_label == season_label)
        .first()
    )
    if existing_season_result is not None:
        existing_season_result.stats = stats
    else:
        db.add(
            TeamSeasonResult(team_id=team.id, league=league, season_label=season_label, stats=stats)
        )

    score = compute_score(league, stats)

    rows = (
        db.query(TeamDailyScore)
        .filter(TeamDailyScore.team_id == team.id, TeamDailyScore.season_label == season_label)
        .all()
    )

    if as_of_date is not None:
        target_date = as_of_date
    else:
        # Same-day retry: a row already written by an earlier run today
        # (wall-clock, not as_of_date -- day 1's row is deliberately dated
        # yesterday, so as_of_date alone can't tell "today's run" apart
        # from "the backdated first row").
        todays_run = next(
            (r for r in rows if r.created_at.astimezone(EASTERN).date() == today_eastern()), None
        )
        if todays_run is not None:
            todays_run.stats = stats
            todays_run.score = score
            return todays_run
        target_date = today_eastern() if rows else today_eastern() - timedelta(days=1)

    existing_day = next((r for r in rows if r.as_of_date == target_date), None)
    if existing_day is not None:
        existing_day.stats = stats
        existing_day.score = score
        return existing_day

    row = TeamDailyScore(
        team_id=team.id,
        league=league,
        season_label=season_label,
        as_of_date=target_date,
        stats=stats,
        score=score,
    )
    db.add(row)
    db.flush()
    return row


if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) != 2:
        print("Usage: python -m app.daily_score_sync <fixture.json>")
        raise SystemExit(1)

    db = SessionLocal()
    try:
        entries = json.load(open(sys.argv[1]))
        synced = 0
        skipped: list[str] = []
        for entry in entries:
            try:
                sync_team_stats(db, entry["league"], entry["team"], entry["stats"])
                synced += 1
            except (TeamNotFoundError, UnsupportedLeagueError) as exc:
                skipped.append(str(exc))
        db.commit()
        print(f"Synced {synced} team(s).")
        for s in skipped:
            print(f"  SKIPPED: {s}")
    finally:
        db.close()
