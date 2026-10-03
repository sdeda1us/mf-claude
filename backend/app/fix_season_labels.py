"""One-off correction for a season_label bug in app/update_live_standings.py:
that script hardcodes a single SEASON_LABEL = "2026-27" applied uniformly
to every league it touches, but per the convention established by
seed_historical_results.py's LEAGUE_SEASONS list, single-calendar-year
leagues (NFL, NCAAF, ATP, WTA among the ones that script covers) should
use "2026", not "2026-27" -- only leagues whose season crosses a new year
(NBA, NHL, EPL, UCL, URC) are correctly "2026-27".

This matters because routers/seasons.py's scoring_summary picks each
team's "most recent" TeamSeasonResult by lexicographic string-sort of
season_label -- if app/daily_score_sync.py starts writing correctly
labeled "2026" rows for NFL/NCAAF/ATP/WTA while these mislabeled
"2026-27" rows still exist, the stray row would keep winning that sort
forever ("2026-27" > "2026").

Run once, before the daily sync starts writing to these leagues:
    python -m app.fix_season_labels
(or `railway ssh -- python -m app.fix_season_labels` in production)

Safe to re-run -- once the mislabeled rows are renamed, there's nothing
left for it to do.

Also means app/update_live_standings.py is retired: rerunning it would
recreate the exact rows this script just fixed. See that module's
docstring.
"""
from app.database import SessionLocal
from app.models import TeamSeasonResult

# league -> (wrong_label, correct_label)
LABEL_FIXES: dict[str, tuple[str, str]] = {
    "NFL": ("2026-27", "2026"),
    "NCAAF": ("2026-27", "2026"),
    "ATP": ("2026-27", "2026"),
    "WTA": ("2026-27", "2026"),
}


def run() -> None:
    db = SessionLocal()
    try:
        fixed = 0
        collisions: list[str] = []
        for league, (wrong_label, correct_label) in LABEL_FIXES.items():
            stray_rows = (
                db.query(TeamSeasonResult)
                .filter(TeamSeasonResult.league == league, TeamSeasonResult.season_label == wrong_label)
                .all()
            )
            for row in stray_rows:
                collision = (
                    db.query(TeamSeasonResult)
                    .filter(
                        TeamSeasonResult.team_id == row.team_id,
                        TeamSeasonResult.season_label == correct_label,
                    )
                    .first()
                )
                if collision is not None:
                    collisions.append(f"{league} team_id={row.team_id}: already has a {correct_label} row")
                    continue
                row.season_label = correct_label
                fixed += 1
        db.commit()
        print(f"Relabeled {fixed} row(s).")
        if collisions:
            print(f"{len(collisions)} collision(s) left untouched -- resolve manually:")
            for c in collisions:
                print(f"  {c}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
