"""One-off backfill for the gap season_labels.ensure_current_season_placeholder
now closes going forward (called at roster-entry creation time, in
auction_service.finalize_active_item and routers/roster.py's commissioner
correction): every team already rostered under the active Season, in a
league the daily sync covers, that doesn't yet have a TeamSeasonResult row
for the current real-world season.

Without this, scoring_summary's "most recent TeamSeasonResult" lookup was
falling back to that team's last REAL season's row for any such team --
e.g. an NBA team rostered before this season tips off reading as last
year's real (nonzero) record instead of 0. update_live_standings.py's old
hardcoded per-league team lists used to paper over most of this by
explicitly zeroing a subset of teams, but never ALL currently-rostered
ones -- hence a handful of teams slipping through.

Run once: python -m app.backfill_season_placeholders
(or `railway ssh -- python -m app.backfill_season_placeholders` in prod)

Safe to re-run -- ensure_current_season_placeholder only ever creates a
missing row, never overwrites an existing one.
"""
from app.database import SessionLocal
from app.models import RosterEntry, Season, SeasonStatus, Team
from app.season_labels import ensure_current_season_placeholder


def run() -> None:
    db = SessionLocal()
    try:
        active_season = db.query(Season).filter(Season.status == SeasonStatus.active).first()
        if active_season is None:
            print("No active season -- nothing to backfill.")
            return

        entries = (
            db.query(RosterEntry)
            .join(Team, RosterEntry.team_id == Team.id)
            .filter(RosterEntry.season_id == active_season.id)
            .all()
        )
        seen_team_ids: set[int] = set()
        created = 0
        for entry in entries:
            if entry.team_id in seen_team_ids:
                continue
            seen_team_ids.add(entry.team_id)
            before = len(db.new)
            ensure_current_season_placeholder(db, entry.team)
            if len(db.new) > before:
                created += 1
        db.commit()
        print(f"Created {created} placeholder TeamSeasonResult row(s).")
    finally:
        db.close()


if __name__ == "__main__":
    run()
