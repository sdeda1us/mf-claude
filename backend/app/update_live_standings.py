"""Updates TeamSeasonResult with the CURRENT, in-progress 2026-27 EPL and
URC standings -- unlike seed_historical_results.py (a one-time load of a
season that's already fully over), this is meant to be re-run periodically
as the real season progresses, each time overwriting the same "2026-27"
row's stats with the latest table. There's no live sports-data feed wired
into this app, so "live" here means "as fresh as the last time someone
(a human, or Claude on request) ran this with a current table looked up
from a reliable source" -- not continuously auto-updating on its own.

Run with: python -m app.update_live_standings
(or `railway ssh -- python -m app.update_live_standings` in production)

Source: Wikipedia's 2026-27 Premier League / 2026-27 United Rugby
Championship season articles.
  EPL table as of 20 September 2026 (5 matches played per team).
  URC table as of 26 September 2026 (1 match played per team -- the season
  just started; every playoff-bracket flag is correctly False this early).
Both are the most recent tables available as of this script's writing
(2026-09-30) -- re-run this (with updated numbers pulled fresh) to refresh
either table later in the season.
"""

from app.database import SessionLocal
from app.models import Team, TeamSeasonResult

SEASON_LABEL = "2026-27"

# name -> (standings_points, goal_differential)
EPL_TABLE: dict[str, tuple[int, int]] = {
    "Manchester City": (15, 8),
    "Arsenal": (12, 4),
    "Brighton & Hove Albion": (10, 11),
    "Brentford": (9, 6),
    "Leeds United": (9, 4),
    "Liverpool": (9, 3),
    "Everton": (9, 3),
    "Hull City": (8, 2),
    "Newcastle United": (8, 0),
    "Chelsea": (7, -2),
    "Ipswich Town": (6, -4),
    "Manchester United": (5, 0),
    "Nottingham Forest": (5, -1),
    "Sunderland": (4, -4),
    "Crystal Palace": (4, -5),
    "Aston Villa": (4, -5),
    "Bournemouth": (3, -2),
    "Coventry City": (3, -9),
    "Fulham": (2, -3),
    "Tottenham Hotspur": (2, -6),
}

# DB name -> (table_points, points_difference). Every team is 1 match into
# the season with no playoff bracket outcomes yet, so made_playoffs and
# every won_* flag are left at their correct-for-right-now False default
# (compute_score's URC branch treats a missing key as falsy).
URC_TABLE: dict[str, tuple[int, int]] = {
    "Bulls": (5, 34),
    "Sharks": (5, 17),
    "Stormers": (5, 14),
    "Glasgow Warriors": (5, 6),
    "Edinburgh": (5, 5),
    "Cardiff": (4, 6),
    "Lions": (4, 1),
    "Benetton": (2, 0),
    "Dragons": (2, 0),
    "Leinster": (2, -1),
    "Ulster": (2, -5),
    "Munster": (1, -6),
    "Scarlets": (1, -6),
    "Ospreys": (1, -17),
    "Connacht": (0, -14),
    "Zebre Parma": (0, -34),
}


def _upsert(db, league: str, name: str, stats: dict) -> bool:
    team = db.query(Team).filter(Team.league == league, Team.name == name).first()
    if team is None:
        print(f"  SKIPPED (no Team row): {league} {name}")
        return False
    existing = (
        db.query(TeamSeasonResult)
        .filter(TeamSeasonResult.team_id == team.id, TeamSeasonResult.season_label == SEASON_LABEL)
        .first()
    )
    if existing:
        existing.stats = stats
    else:
        db.add(TeamSeasonResult(team_id=team.id, league=league, season_label=SEASON_LABEL, stats=stats))
    return True


def update() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for name, (points, gd) in EPL_TABLE.items():
            if _upsert(db, "EPL", name, {"standings_points": points, "goal_differential": gd}):
                updated += 1
        for name, (points, diff) in URC_TABLE.items():
            stats = {
                "table_points": points,
                "points_difference": diff,
                "made_playoffs": False,
                "won_quarterfinal": False,
                "won_semifinal": False,
                "won_final": False,
            }
            if _upsert(db, "URC", name, stats):
                updated += 1
        db.commit()
        print(f"Updated {updated} team-season rows for {SEASON_LABEL}.")
    finally:
        db.close()


if __name__ == "__main__":
    update()
