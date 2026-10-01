"""Updates TeamSeasonResult with the CURRENT, in-progress 2026-27 standings
for every league in routers.seasons.SCORING_SUMMARY_LEAGUES -- unlike
seed_historical_results.py (a one-time load of a season that's already
fully over), this is meant to be re-run periodically as the real season
progresses, each time overwriting the same "2026-27" row's stats with the
latest table. There's no live sports-data feed wired into this app, so
"live" here means "as fresh as the last time someone (a human, or Claude
on request) ran this with a current table looked up from a reliable
source" -- not continuously auto-updating on its own.

Only ever seeds rows for teams/countries someone's actually drafted (see
each *_TABLE below) -- undrafted teams in a league stay without a
"2026-27" row entirely, which scoring_summary() already treats as a
silent 0, same as a league that hasn't started yet.

NBA/ATP/WTA are deliberately all-zero: the 2026-27 NBA season and the
2026-27 tennis major window (first major is the Australian Open, due
January 2027) hadn't started as of this writing, so these rows exist
only to shadow stale prior-season ("2025-26"/"2025") rows that would
otherwise read as "most recent" by default -- without an explicit zeroed
"2026-27" row, scoring_summary would show last season's real (nonzero)
numbers for a league that hasn't actually played a game yet.

Run with: python -m app.update_live_standings
(or `railway ssh -- python -m app.update_live_standings` in production)

Source: Wikipedia's 2026-27 season articles for each league, as of
2026-10-01 (EPL/URC tables are a few days older, from this script's first
version on 2026-09-30).
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


# name -> (wins, ties), through Week 3 (games as of 2026-10-01). NFL's
# compute_score only uses wins/ties, not losses, so losses aren't tracked
# here. No playoff round has happened yet (regular season just started),
# so every won_* flag is correctly left at its False default.
NFL_TABLE: dict[str, tuple[int, int]] = {
    "Baltimore Ravens": (2, 0),
    "Buffalo Bills": (3, 0),
    "Chicago Bears": (2, 0),
    "Cincinnati Bengals": (2, 0),
    "Dallas Cowboys": (1, 0),
    "Denver Broncos": (2, 0),
    "Detroit Lions": (2, 0),
    "Green Bay Packers": (1, 0),
    "Houston Texans": (0, 0),
    "Jacksonville Jaguars": (2, 0),
    "Kansas City Chiefs": (3, 0),
    "Las Vegas Raiders": (3, 0),
    "Los Angeles Chargers": (0, 0),
    "Los Angeles Rams": (1, 0),
    "Minnesota Vikings": (3, 0),
    "New England Patriots": (1, 0),
    "New Orleans Saints": (1, 0),
    "Philadelphia Eagles": (2, 0),
    "Pittsburgh Steelers": (2, 0),
    "San Francisco 49ers": (3, 0),
    "Seattle Seahawks": (2, 0),
    "Tampa Bay Buccaneers": (0, 0),
}

# The 2026-27 NBA season hadn't tipped off as of this writing (projected to
# open ~Oct 20, 2026) -- every rostered team gets an explicit all-zero row
# so this shadows each team's real, nonzero "2025-26" row rather than
# scoring_summary falling back to show last season's actual standings.
NBA_TABLE_TEAMS: list[str] = [
    "Atlanta Hawks", "Boston Celtics", "Cleveland Cavaliers", "Dallas Mavericks",
    "Denver Nuggets", "Detroit Pistons", "Golden State Warriors", "Houston Rockets",
    "Indiana Pacers", "Los Angeles Lakers", "Miami Heat", "Minnesota Timberwolves",
    "New York Knicks", "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers",
    "Phoenix Suns", "Portland Trail Blazers", "San Antonio Spurs", "Toronto Raptors",
    "Utah Jazz", "Washington Wizards",
]

# Same reasoning as NBA_TABLE_TEAMS: the 2026-27 majors window hasn't
# opened yet (first major is the Australian Open, due January 2027), so
# every rostered country gets an explicit all-zero row to shadow its real
# "2025" row.
ATP_TABLE_COUNTRIES: list[str] = [
    "Argentina", "Australia", "Czech Republic", "France", "Germany",
    "Great Britain", "Italy", "Russia", "Serbia", "Spain", "United States",
]
WTA_TABLE_COUNTRIES: list[str] = [
    "Australia", "Belarus", "Czech Republic", "France", "Kazakhstan",
    "Poland", "Russia", "Spain", "Ukraine", "United States",
]


# name -> (points, goal_differential), through Matchday 1 (played Sept
# 8-10, 2026; Matchday 2 is Oct 13-14, 2026, so every club is 1 match in
# as of this writing). No knockout round has happened yet, so every
# made_final_* and won_final flag is correctly left at its False default.
UCL_TABLE: dict[str, tuple[int, int]] = {
    "Arsenal": (3, 1),
    "Aston Villa": (3, 1),
    "Atlético Madrid": (0, -1),
    "Barcelona": (3, 4),
    "Bayern Munich": (3, 5),
    "Borussia Dortmund": (3, 1),
    "Galatasaray": (0, -2),
    "Inter Milan": (0, -1),
    "Liverpool": (3, 1),
    "Manchester City": (3, 2),
    "Manchester United": (3, 4),
    "Napoli": (0, -1),
    "Paris Saint-Germain": (3, 5),
    "Porto": (0, -2),
    "RB Leipzig": (0, -3),
    "Real Betis": (3, 1),
    "Real Madrid": (3, 1),
    "Roma": (1, 0),
    "Sporting CP": (3, 2),
}


# name -> (wins, reg_losses, ot_losses), through games played Sept 29-30,
# 2026 (the season just started; most teams haven't played yet, legitimately
# 0-0-0). No playoff round has happened yet, so every made_playoffs/won_*
# flag is correctly left at its False default.
NHL_TABLE: dict[str, tuple[int, int, int]] = {
    "Anaheim Ducks": (0, 0, 0),
    "Boston Bruins": (1, 0, 0),
    "Buffalo Sabres": (0, 0, 0),
    "Carolina Hurricanes": (0, 0, 1),
    "Colorado Avalanche": (1, 0, 0),
    "Columbus Blue Jackets": (0, 0, 0),
    "Dallas Stars": (0, 0, 0),
    "Edmonton Oilers": (0, 0, 1),
    "Florida Panthers": (1, 0, 0),
    "Los Angeles Kings": (0, 1, 0),
    "Minnesota Wild": (0, 0, 0),
    "Montreal Canadiens": (1, 0, 0),
    "New Jersey Devils": (0, 0, 0),
    "Ottawa Senators": (0, 0, 0),
    "Philadelphia Flyers": (0, 1, 0),
    "San Jose Sharks": (0, 0, 0),
    "St. Louis Blues": (0, 0, 0),
    "Tampa Bay Lightning": (0, 0, 0),
    "Toronto Maple Leafs": (1, 1, 0),
    "Utah Mammoth": (0, 0, 0),
    "Vegas Golden Knights": (1, 0, 0),
    "Washington Capitals": (0, 0, 0),
}


# name -> (wins, reg_season_losses), through games played as of 2026-10-01
# (roughly 4-5 games into the season). No bowl/playoff bid is decided this
# early, so playoff_bid/championship_bid/championship_win are all
# correctly left at their False default.
NCAAF_TABLE: dict[str, tuple[int, int]] = {
    "Alabama Crimson Tide": (4, 0),
    "Auburn Tigers": (3, 1),
    "BYU Cougars": (3, 0),
    "Florida Gators": (4, 0),
    "Georgia Bulldogs": (4, 0),
    "Indiana Hoosiers": (4, 0),
    "Iowa Hawkeyes": (4, 0),
    "LSU Tigers": (3, 1),
    "Louisville Cardinals": (2, 2),
    "Miami (FL) Hurricanes": (4, 0),
    "Michigan Wolverines": (3, 1),
    "Nebraska Cornhuskers": (4, 0),
    "Notre Dame Fighting Irish": (4, 0),
    "Ohio State Buckeyes": (3, 1),
    "Oklahoma Sooners": (2, 2),
    "Ole Miss Rebels": (3, 1),
    "Oregon Ducks": (3, 1),
    "Penn State Nittany Lions": (3, 1),
    "Tennessee Volunteers": (3, 1),
    "Texas A&M Aggies": (2, 2),
    "Texas Longhorns": (4, 0),
    "Texas Tech Red Raiders": (4, 0),
    "USC Trojans": (4, 1),
    "Vanderbilt Commodores": (3, 1),
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
        for name, (wins, ties) in NFL_TABLE.items():
            if _upsert(db, "NFL", name, {"wins": wins, "ties": ties}):
                updated += 1
        for name, (points, gd) in UCL_TABLE.items():
            stats = {
                "points": points,
                "goal_differential": gd,
                "made_final_24": False,
                "made_final_16": False,
                "made_final_8": False,
                "made_final_4": False,
                "made_final_2": False,
                "won_final": False,
            }
            if _upsert(db, "UCL", name, stats):
                updated += 1
        for name, (wins, reg_losses, ot_losses) in NHL_TABLE.items():
            stats = {
                "wins": wins,
                "reg_losses": reg_losses,
                "ot_losses": ot_losses,
                "made_playoffs": False,
                "won_round1": False,
                "won_round2": False,
                "won_conf_champ": False,
                "won_cup": False,
            }
            if _upsert(db, "NHL", name, stats):
                updated += 1
        for name, (wins, losses) in NCAAF_TABLE.items():
            stats = {
                "wins": wins,
                "reg_season_losses": losses,
                "playoff_bid": False,
                "playoff_wins": 0,
                "playoff_bye": False,
                "championship_bid": False,
                "championship_win": False,
            }
            if _upsert(db, "NCAAF", name, stats):
                updated += 1
        zero_nba_stats = {
            "wins": 0,
            "losses": 0,
            "made_playoffs": False,
            "won_round1": False,
            "won_round2": False,
            "won_conf_champ": False,
            "won_nba_champ": False,
        }
        for name in NBA_TABLE_TEAMS:
            if _upsert(db, "NBA", name, zero_nba_stats):
                updated += 1
        zero_tennis_stats = {
            "round_1_wins": 0,
            "round_2_wins": 0,
            "round_3_wins": 0,
            "round_4_wins": 0,
            "quarterfinal_wins": 0,
            "semifinal_wins": 0,
            "final_wins": 0,
        }
        for name in ATP_TABLE_COUNTRIES:
            if _upsert(db, "ATP", name, zero_tennis_stats):
                updated += 1
        for name in WTA_TABLE_COUNTRIES:
            if _upsert(db, "WTA", name, zero_tennis_stats):
                updated += 1
        db.commit()
        print(f"Updated {updated} team-season rows for {SEASON_LABEL}.")
    finally:
        db.close()


if __name__ == "__main__":
    update()
