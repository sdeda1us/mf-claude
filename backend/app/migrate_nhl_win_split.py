"""One-off migration for the NHL regulation/OT-SO win-split scoring change:
compute_score's NHL branch now reads reg_wins/ot_so_wins instead of a
single combined wins count, and OT/shootout losses no longer carry a
bonus (ot_losses is dropped from the formula entirely). Without this,
every already-stored NHL TeamSeasonResult/TeamDailyScore row (all under
the old {wins, reg_losses, ot_losses, ...} shape) would read as if the
team had 0 regulation wins and 0 OT/SO wins until its next daily sync --
compute_score defensively .get()s those two new keys rather than
crashing, but the displayed score would be wrong (far too low) in the
meantime.

Renames in place, for every row still in the old shape: wins -> reg_wins
(the best available approximation -- there's no way to retroactively
split historical "wins" into regulation vs. OT/SO from this data alone,
so this assumes they were all regulation wins, which exactly preserves
each team's old score for the reg-win/reg-loss terms); adds
ot_so_wins = 0; renames ot_losses -> ot_so_losses (carried over for data
completeness even though it no longer affects score). reg_losses is
untouched -- same key, same meaning, no migration needed.

A real breakdown (how many of each team's wins came in regulation vs.
OT/shootout) arrives the next time the daily sync researches NHL, at
which point this placeholder gets overwritten with real numbers same as
any other day's sync.

Run once: python -m app.migrate_nhl_win_split
(or `railway ssh -- python -m app.migrate_nhl_win_split` in production)

Safe to re-run -- rows already in the new shape (has reg_wins) are left
untouched.
"""
from app.database import SessionLocal
from app.models import TeamDailyScore, TeamSeasonResult


def _migrate_stats(stats: dict) -> dict | None:
    """Returns a migrated copy, or None if this row is already new-shape
    (or isn't NHL's old shape at all) and needs no change."""
    if "reg_wins" in stats or "wins" not in stats:
        return None
    migrated = dict(stats)
    migrated["reg_wins"] = migrated.pop("wins")
    migrated["ot_so_wins"] = 0
    if "ot_losses" in migrated:
        migrated["ot_so_losses"] = migrated.pop("ot_losses")
    return migrated


def run() -> None:
    db = SessionLocal()
    try:
        season_result_count = 0
        for row in db.query(TeamSeasonResult).filter(TeamSeasonResult.league == "NHL").all():
            migrated = _migrate_stats(row.stats)
            if migrated is not None:
                row.stats = migrated
                season_result_count += 1

        daily_score_count = 0
        for row in db.query(TeamDailyScore).filter(TeamDailyScore.league == "NHL").all():
            migrated = _migrate_stats(row.stats)
            if migrated is not None:
                row.stats = migrated
                daily_score_count += 1

        db.commit()
        print(
            f"Migrated {season_result_count} TeamSeasonResult row(s) and "
            f"{daily_score_count} TeamDailyScore row(s)."
        )
    finally:
        db.close()


if __name__ == "__main__":
    run()
