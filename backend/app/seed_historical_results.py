"""Loads real results for each league's most recently completed season, for
the "example scores" page (what each team would have scored under the wiki's
rules). One-time historical load, separate from seed.py's user/team seeding.

Run with: python -m app.seed_historical_results
(or `railway ssh -- python -m app.seed_historical_results` in production)

Season covered per league (all fully concluded as of this writing):
  MLB 2025, NFL 2025, NBA 2025-26, NHL 2025-26, EPL 2025-26, NCAAF 2025,
  NCAAMB 2025-26, NCAAWB 2025-26, ATP 2025 (4 majors), WTA 2025 (4 majors),
  PGA 2026 (4 majors), LPGA 2026 (4 counted majors), F1 2025, WNBA 2025,
  MLS 2025, URC 2025-26, IPL 2026, NWSL 2025, TDF 2026 (top 3 only)

Sources: Wikipedia season/playoff articles for each league (final standings,
playoff brackets), cross-checked for internal consistency (game counts,
bracket progression). One documented gap: NCAAF's bowl/playoff-loss
identification (which losses score 0 instead of -6) is sourced from the
full CFP bracket plus a consolidated list of the season's ~35 non-playoff
bowl games; a handful of smaller bowls not covered by that source would
fall back to being scored as a regular-season loss (-6) rather than the
bowl-loss exception (0) if missed. Everything else here (records,
division/round winners, EPL points/GD, NHL W/L/OTL) is sourced directly.

The 6 leagues added after the original 6 (NCAAMB, NCAAWB, ATP, WTA, PGA,
LPGA) are DELIBERATELY SCOPED DOWN given their scale (~360 college hoops
teams, ~70 tennis countries, 26 golf letters x deep major fields). Each
section below documents its own specific scope limits; the shared theme is:
only the top of the bracket/leaderboard is populated, and a couple of
scoring-rule inputs are left at their zero/false default everywhere (called
out per section) rather than researched exhaustively. Teams/countries/
letters with no data simply get no TeamSeasonResult row — seed() already
handles that gracefully (only names present in a league's names_map are
processed).
"""

from sqlalchemy.exc import IntegrityError

from app.database import Base, SessionLocal, engine
from app.models import Team, TeamSeasonResult

# ---------------------------------------------------------------------------
# MLB 2025 — regular season records, division winners, postseason bracket
# ---------------------------------------------------------------------------

MLB_RECORDS = {
    "Toronto Blue Jays": (94, 68), "New York Yankees": (94, 68), "Boston Red Sox": (89, 73),
    "Tampa Bay Rays": (77, 85), "Baltimore Orioles": (75, 87),
    "Cleveland Guardians": (88, 74), "Detroit Tigers": (87, 75), "Kansas City Royals": (82, 80),
    "Minnesota Twins": (70, 92), "Chicago White Sox": (60, 102),
    "Seattle Mariners": (90, 72), "Houston Astros": (87, 75), "Texas Rangers": (81, 81),
    "Athletics": (76, 86), "Los Angeles Angels": (72, 90),
    "Philadelphia Phillies": (96, 66), "New York Mets": (83, 79), "Miami Marlins": (79, 83),
    "Atlanta Braves": (76, 86), "Washington Nationals": (66, 96),
    "Milwaukee Brewers": (97, 65), "Chicago Cubs": (92, 70), "Cincinnati Reds": (83, 79),
    "St. Louis Cardinals": (78, 84), "Pittsburgh Pirates": (71, 91),
    "Los Angeles Dodgers": (93, 69), "San Diego Padres": (90, 72), "San Francisco Giants": (81, 81),
    "Arizona Diamondbacks": (80, 82), "Colorado Rockies": (43, 119),
}
MLB_DIVISION_WINNERS = {
    "Toronto Blue Jays", "Cleveland Guardians", "Seattle Mariners",
    "Philadelphia Phillies", "Milwaukee Brewers", "Los Angeles Dodgers",
}
# ALDS/NLDS winners (advanced to LCS)
MLB_DS_WINNERS = {"Toronto Blue Jays", "Seattle Mariners", "Milwaukee Brewers", "Los Angeles Dodgers"}
# ALCS/NLCS winners (pennant)
MLB_PENNANT_WINNERS = {"Toronto Blue Jays", "Los Angeles Dodgers"}
MLB_WS_WINNER = "Los Angeles Dodgers"


def mlb_stats(name: str) -> dict:
    wins, losses = MLB_RECORDS[name]
    return {
        "wins": wins,
        "losses": losses,
        "won_division": name in MLB_DIVISION_WINNERS,
        "won_ds": name in MLB_DS_WINNERS,
        "won_pennant": name in MLB_PENNANT_WINNERS,
        "won_ws": name == MLB_WS_WINNER,
    }


# ---------------------------------------------------------------------------
# NFL 2025 — regular season records, playoff bracket (Super Bowl LX)
# ---------------------------------------------------------------------------

NFL_RECORDS = {
    "New England Patriots": (14, 3, 0), "Buffalo Bills": (12, 5, 0), "Miami Dolphins": (7, 10, 0), "New York Jets": (3, 14, 0),
    "Pittsburgh Steelers": (10, 7, 0), "Baltimore Ravens": (8, 9, 0), "Cincinnati Bengals": (6, 11, 0), "Cleveland Browns": (5, 12, 0),
    "Jacksonville Jaguars": (13, 4, 0), "Houston Texans": (12, 5, 0), "Indianapolis Colts": (8, 9, 0), "Tennessee Titans": (3, 14, 0),
    "Denver Broncos": (14, 3, 0), "Los Angeles Chargers": (11, 6, 0), "Kansas City Chiefs": (6, 11, 0), "Las Vegas Raiders": (3, 14, 0),
    "Philadelphia Eagles": (11, 6, 0), "Dallas Cowboys": (7, 9, 1), "Washington Commanders": (5, 12, 0), "New York Giants": (4, 13, 0),
    "Chicago Bears": (11, 6, 0), "Green Bay Packers": (9, 7, 1), "Minnesota Vikings": (9, 8, 0), "Detroit Lions": (9, 8, 0),
    "Carolina Panthers": (8, 9, 0), "Tampa Bay Buccaneers": (8, 9, 0), "Atlanta Falcons": (8, 9, 0), "New Orleans Saints": (6, 11, 0),
    "Seattle Seahawks": (14, 3, 0), "Los Angeles Rams": (12, 5, 0), "San Francisco 49ers": (12, 5, 0), "Arizona Cardinals": (3, 14, 0),
}
# Won Wild Card round, or had a first-round bye
NFL_ROUND1_OR_BYE = {
    "Denver Broncos", "New England Patriots", "Houston Texans", "Buffalo Bills",
    "Seattle Seahawks", "Los Angeles Rams", "Chicago Bears", "San Francisco 49ers",
}
# Won Divisional round
NFL_ROUND2 = {"Denver Broncos", "New England Patriots", "Seattle Seahawks", "Los Angeles Rams"}
# Won Conference Championship
NFL_CONF_CHAMPS = {"New England Patriots", "Seattle Seahawks"}
NFL_SB_WINNER = "Seattle Seahawks"


def nfl_stats(name: str) -> dict:
    wins, losses, ties = NFL_RECORDS[name]
    return {
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "won_round1_or_bye": name in NFL_ROUND1_OR_BYE,
        "won_round2": name in NFL_ROUND2,
        "won_conf_champ": name in NFL_CONF_CHAMPS,
        "won_sb": name == NFL_SB_WINNER,
    }


# ---------------------------------------------------------------------------
# NBA 2025-26 — regular season records, playoff bracket (Knicks champions)
# ---------------------------------------------------------------------------

NBA_RECORDS = {
    "Detroit Pistons": (60, 22), "Boston Celtics": (56, 26), "New York Knicks": (53, 29),
    "Cleveland Cavaliers": (52, 30), "Toronto Raptors": (46, 36), "Atlanta Hawks": (46, 36),
    "Philadelphia 76ers": (45, 37), "Orlando Magic": (45, 37), "Charlotte Hornets": (44, 38),
    "Miami Heat": (43, 39), "Milwaukee Bucks": (32, 50), "Chicago Bulls": (31, 51),
    "Brooklyn Nets": (20, 62), "Indiana Pacers": (19, 63), "Washington Wizards": (17, 65),
    "Oklahoma City Thunder": (64, 18), "San Antonio Spurs": (62, 20), "Denver Nuggets": (54, 28),
    "Los Angeles Lakers": (53, 29), "Houston Rockets": (52, 30), "Minnesota Timberwolves": (49, 33),
    "Phoenix Suns": (45, 37), "Portland Trail Blazers": (42, 40), "Los Angeles Clippers": (42, 40),
    "Golden State Warriors": (37, 45), "New Orleans Pelicans": (26, 56), "Dallas Mavericks": (26, 56),
    "Memphis Grizzlies": (25, 57), "Sacramento Kings": (22, 60), "Utah Jazz": (22, 60),
}
NBA_MADE_PLAYOFFS = {
    "Detroit Pistons", "Boston Celtics", "New York Knicks", "Cleveland Cavaliers",
    "Toronto Raptors", "Atlanta Hawks", "Philadelphia 76ers", "Orlando Magic",
    "Oklahoma City Thunder", "San Antonio Spurs", "Denver Nuggets", "Los Angeles Lakers",
    "Houston Rockets", "Minnesota Timberwolves", "Phoenix Suns", "Golden State Warriors",
}
NBA_ROUND1_WINNERS = {
    "Detroit Pistons", "Philadelphia 76ers", "New York Knicks", "Cleveland Cavaliers",
    "Oklahoma City Thunder", "San Antonio Spurs", "Minnesota Timberwolves", "Los Angeles Lakers",
}
NBA_ROUND2_WINNERS = {"Cleveland Cavaliers", "New York Knicks", "Oklahoma City Thunder", "San Antonio Spurs"}
NBA_CONF_CHAMPS = {"New York Knicks", "San Antonio Spurs"}
NBA_CHAMPION = "New York Knicks"


def nba_stats(name: str) -> dict:
    wins, losses = NBA_RECORDS[name]
    return {
        "wins": wins,
        "losses": losses,
        "made_playoffs": name in NBA_MADE_PLAYOFFS,
        "won_round1": name in NBA_ROUND1_WINNERS,
        "won_round2": name in NBA_ROUND2_WINNERS,
        "won_conf_champ": name in NBA_CONF_CHAMPS,
        "won_nba_champ": name == NBA_CHAMPION,
    }


# ---------------------------------------------------------------------------
# NHL 2025-26 — regular season W-L-OTL, playoff bracket (Hurricanes champions)
# ---------------------------------------------------------------------------

NHL_RECORDS = {
    # (wins, losses, otl)
    "Buffalo Sabres": (50, 23, 9), "Tampa Bay Lightning": (50, 26, 6), "Montreal Canadiens": (48, 24, 10),
    "Boston Bruins": (45, 27, 10), "Ottawa Senators": (44, 27, 11), "Toronto Maple Leafs": (32, 36, 14),
    "Detroit Red Wings": (41, 31, 10), "Florida Panthers": (40, 38, 4),
    "Carolina Hurricanes": (53, 22, 7), "Pittsburgh Penguins": (41, 25, 16), "Philadelphia Flyers": (43, 27, 12),
    "New York Rangers": (34, 39, 9), "New Jersey Devils": (42, 37, 3), "Washington Capitals": (43, 30, 9),
    "Columbus Blue Jackets": (40, 30, 12), "New York Islanders": (43, 34, 5),
    "Colorado Avalanche": (55, 16, 11), "Dallas Stars": (50, 20, 12), "Minnesota Wild": (46, 24, 12),
    "Utah Mammoth": (43, 33, 6), "St. Louis Blues": (37, 33, 12), "Nashville Predators": (38, 34, 10),
    "Winnipeg Jets": (35, 35, 12), "Chicago Blackhawks": (29, 39, 14),
    "Vegas Golden Knights": (39, 26, 17), "Edmonton Oilers": (41, 30, 11), "Anaheim Ducks": (43, 33, 6),
    "Los Angeles Kings": (35, 27, 20), "Vancouver Canucks": (25, 49, 8), "Calgary Flames": (34, 39, 9),
    "San Jose Sharks": (39, 35, 8), "Seattle Kraken": (34, 37, 11),
}
NHL_MADE_PLAYOFFS = {
    "Buffalo Sabres", "Tampa Bay Lightning", "Montreal Canadiens", "Boston Bruins", "Ottawa Senators",
    "Carolina Hurricanes", "Pittsburgh Penguins", "Philadelphia Flyers",
    "Colorado Avalanche", "Dallas Stars", "Minnesota Wild", "Utah Mammoth",
    "Vegas Golden Knights", "Edmonton Oilers", "Anaheim Ducks", "Los Angeles Kings",
}
NHL_ROUND1_WINNERS = {
    "Buffalo Sabres", "Montreal Canadiens", "Carolina Hurricanes", "Philadelphia Flyers",
    "Colorado Avalanche", "Minnesota Wild", "Vegas Golden Knights", "Anaheim Ducks",
}
NHL_ROUND2_WINNERS = {"Montreal Canadiens", "Carolina Hurricanes", "Colorado Avalanche", "Vegas Golden Knights"}
NHL_CONF_CHAMPS = {"Carolina Hurricanes", "Vegas Golden Knights"}
NHL_CUP_WINNER = "Carolina Hurricanes"


def nhl_stats(name: str) -> dict:
    wins, losses, otl = NHL_RECORDS[name]
    return {
        "wins": wins,
        "reg_losses": losses,
        "ot_losses": otl,
        "made_playoffs": name in NHL_MADE_PLAYOFFS,
        "won_round1": name in NHL_ROUND1_WINNERS,
        "won_round2": name in NHL_ROUND2_WINNERS,
        "won_conf_champ": name in NHL_CONF_CHAMPS,
        "won_cup": name == NHL_CUP_WINNER,
    }


# ---------------------------------------------------------------------------
# EPL 2025-26 — final table points & goal differential
# ---------------------------------------------------------------------------

EPL_TABLE = {
    # (points, goal_differential)
    "Arsenal": (85, 44), "Manchester City": (78, 42), "Manchester United": (71, 19),
    "Aston Villa": (65, 7), "Liverpool": (60, 10), "Bournemouth": (57, 4),
    "Sunderland": (54, -6), "Brighton & Hove Albion": (53, 6), "Brentford": (53, 3),
    "Chelsea": (52, 6), "Fulham": (52, -4), "Newcastle United": (49, -2),
    "Everton": (49, -3), "Leeds United": (47, -7), "Crystal Palace": (45, -10),
    "Nottingham Forest": (44, -3), "Tottenham Hotspur": (41, -9), "West Ham United": (39, -19),
    "Burnley": (22, -37), "Wolverhampton Wanderers": (20, -41),
}


def epl_stats(name: str) -> dict:
    points, gd = EPL_TABLE[name]
    return {"standings_points": points, "goal_differential": gd}


# ---------------------------------------------------------------------------
# NCAAF 2025 — regular season + bowl/playoff records, 12-team CFP bracket
# (Indiana national champions). Two 2026 FBS members — North Dakota State
# and Sacramento State — were still FCS in 2025 and have no record here;
# they're skipped the same way relegated EPL clubs are.
# ---------------------------------------------------------------------------

NCAAF_RECORDS = {
    # (wins, total losses, including bowl/playoff) — SEC
    "Alabama Crimson Tide": (11, 4), "Arkansas Razorbacks": (2, 10), "Auburn Tigers": (5, 7), "Florida Gators": (4, 8),
    "Georgia Bulldogs": (12, 2), "Kentucky Wildcats": (5, 7), "LSU Tigers": (7, 6), "Mississippi State Bulldogs": (5, 8),
    "Missouri Tigers": (8, 5), "Oklahoma Sooners": (10, 3), "Ole Miss Rebels": (13, 2), "South Carolina Gamecocks": (4, 8),
    "Tennessee Volunteers": (8, 5), "Texas Longhorns": (10, 3), "Texas A&M Aggies": (11, 2), "Vanderbilt Commodores": (10, 3),
    # Big Ten
    "Illinois Fighting Illini": (9, 4), "Indiana Hoosiers": (16, 0), "Iowa Hawkeyes": (9, 4), "Maryland Terrapins": (4, 8),
    "Michigan Wolverines": (9, 4), "Michigan State Spartans": (4, 8), "Minnesota Golden Gophers": (8, 5), "Nebraska Cornhuskers": (7, 6),
    "Northwestern Wildcats": (7, 6), "Ohio State Buckeyes": (12, 2), "Oregon Ducks": (13, 2), "Penn State Nittany Lions": (7, 6),
    "Purdue Boilermakers": (2, 10), "Rutgers Scarlet Knights": (5, 7), "UCLA Bruins": (3, 9), "USC Trojans": (9, 4),
    "Washington Huskies": (9, 4), "Wisconsin Badgers": (4, 8),
    # ACC
    "Boston College Eagles": (2, 10), "California Golden Bears": (7, 6), "Clemson Tigers": (7, 6), "Duke Blue Devils": (9, 5),
    "Florida State Seminoles": (5, 7), "Georgia Tech Yellow Jackets": (9, 4), "Louisville Cardinals": (9, 4), "Miami (FL) Hurricanes": (13, 3),
    "NC State Wolfpack": (8, 5), "North Carolina Tar Heels": (4, 8), "Pittsburgh Panthers": (8, 5), "SMU Mustangs": (9, 4),
    "Stanford Cardinal": (4, 8), "Syracuse Orange": (3, 9), "Virginia Cavaliers": (11, 3), "Virginia Tech Hokies": (3, 9),
    "Wake Forest Demon Deacons": (9, 4),
    # Big 12
    "Arizona Wildcats": (9, 4), "Arizona State Sun Devils": (8, 5), "Baylor Bears": (5, 7), "BYU Cougars": (12, 2),
    "Cincinnati Bearcats": (7, 6), "Colorado Buffaloes": (3, 9), "Houston Cougars": (10, 3), "Iowa State Cyclones": (8, 4),
    "Kansas Jayhawks": (5, 7), "Kansas State Wildcats": (6, 6), "Oklahoma State Cowboys": (1, 11), "TCU Horned Frogs": (9, 4),
    "Texas Tech Red Raiders": (12, 2), "UCF Knights": (5, 7), "Utah Utes": (11, 2), "West Virginia Mountaineers": (4, 8),
    # Pac-12 (2025 records — Oregon State/Washington State played as a 2-team
    # rump conference in 2025; the rebuilt 8-team Pac-12 starts 2026)
    "Boise State Broncos": (9, 5), "Colorado State Rams": (2, 10), "Fresno State Bulldogs": (9, 4),
    "Oregon State Beavers": (2, 10), "San Diego State Aztecs": (9, 4), "Texas State Bobcats": (7, 6),
    "Utah State Aggies": (6, 7), "Washington State Cougars": (7, 6),
    # Mountain West (North Dakota State skipped — see module docstring)
    "Air Force Falcons": (4, 8), "Hawaii Rainbow Warriors": (9, 4), "Nevada Wolf Pack": (3, 9), "New Mexico Lobos": (9, 4),
    "Northern Illinois Huskies": (3, 9), "San Jose State Spartans": (3, 9), "UNLV Rebels": (10, 4),
    "UTEP Miners": (2, 10), "Wyoming Cowboys": (4, 8),
    # American
    "Army Black Knights": (7, 6), "Charlotte 49ers": (1, 11), "East Carolina Pirates": (9, 4), "Florida Atlantic Owls": (4, 8),
    "Memphis Tigers": (8, 5), "Navy Midshipmen": (11, 2), "North Texas Mean Green": (12, 2), "Rice Owls": (5, 8),
    "South Florida Bulls": (9, 4), "Temple Owls": (5, 7), "Tulane Green Wave": (11, 3), "Tulsa Golden Hurricane": (4, 8),
    "UAB Blazers": (4, 8), "UTSA Roadrunners": (7, 6),
    # Sun Belt
    "Appalachian State Mountaineers": (5, 8), "Arkansas State Red Wolves": (7, 6), "Coastal Carolina Chanticleers": (6, 7),
    "Georgia Southern Eagles": (7, 6), "Georgia State Panthers": (1, 11), "James Madison Dukes": (12, 2),
    "Louisiana Ragin' Cajuns": (6, 7), "Louisiana-Monroe Warhawks": (3, 9), "Louisiana Tech Bulldogs": (8, 5),
    "Marshall Thundering Herd": (5, 7), "Old Dominion Monarchs": (10, 3), "South Alabama Jaguars": (4, 8),
    "Southern Miss Golden Eagles": (7, 6), "Troy Trojans": (8, 6),
    # MAC (Sacramento State skipped — see module docstring)
    "Akron Zips": (5, 7), "Ball State Cardinals": (4, 8), "Bowling Green Falcons": (4, 8), "Buffalo Bulls": (5, 7),
    "Central Michigan Chippewas": (7, 6), "Eastern Michigan Eagles": (4, 8), "Kent State Golden Flashes": (5, 7),
    "Miami (OH) RedHawks": (7, 7), "Ohio Bobcats": (9, 4), "Toledo Rockets": (8, 5), "UMass Minutemen": (0, 12),
    "Western Michigan Broncos": (10, 4),
    # Conference USA
    "Delaware Blue Hens": (7, 6), "FIU Panthers": (7, 6), "Jacksonville State Gamecocks": (9, 5), "Kennesaw State Owls": (10, 4),
    "Liberty Flames": (4, 8), "Middle Tennessee Blue Raiders": (3, 9), "Missouri State Bears": (7, 6),
    "New Mexico State Aggies": (4, 8), "Sam Houston Bearkats": (2, 10), "Western Kentucky Hilltoppers": (9, 4),
    # FBS Independents
    "Notre Dame Fighting Irish": (10, 2), "UConn Huskies": (9, 4),
}

# 12-team CFP field. Seeds 1-4 got byes; seeds 5-12 played a first round game.
NCAAF_PLAYOFF_BID = {
    "Indiana Hoosiers", "Ohio State Buckeyes", "Georgia Bulldogs", "Texas Tech Red Raiders", "Oregon Ducks", "Ole Miss Rebels",
    "Texas A&M Aggies", "Oklahoma Sooners", "Alabama Crimson Tide", "Miami (FL) Hurricanes", "Tulane Green Wave", "James Madison Dukes",
}
# Non-championship playoff wins (round 1 / quarterfinal / semifinal), each
# worth +10 on top of the base +12 per-win score for that same game.
NCAAF_PLAYOFF_WINS = {
    "Alabama Crimson Tide": 1,       # beat Oklahoma in round 1, lost QF to Indiana
    "Ole Miss Rebels": 2,       # beat Tulane, beat Georgia; lost semifinal to Miami
    "Oregon Ducks": 2,          # beat James Madison, beat Texas Tech; lost semifinal to Indiana
    "Miami (FL) Hurricanes": 3,        # beat Texas A&M, Ohio State, Ole Miss; lost championship to Indiana
    "Indiana Hoosiers": 2,             # bye, beat Alabama (QF) and Oregon (SF); championship win tracked separately
}
NCAAF_CHAMPIONSHIP_BID = {"Indiana Hoosiers", "Miami (FL) Hurricanes"}
NCAAF_CHAMPIONSHIP_WINNER = "Indiana Hoosiers"

# Teams whose season ended in a bowl or playoff-round loss (that specific
# loss scores 0, not -6 — see league_rules.compute_score). Sourced from the
# full 2025-26 bowl schedule/results plus the CFP bracket above.
NCAAF_BOWL_LOSERS = {
    # Non-playoff bowls
    "Boise State Broncos", "Troy Trojans", "South Florida Bulls", "Louisiana Ragin' Cajuns", "Missouri State Bears",
    "Kennesaw State Owls", "Memphis Tigers", "Utah State Aggies", "Toledo Rockets", "Southern Miss Golden Eagles",
    "UNLV Rebels", "California Golden Bears", "Central Michigan Chippewas", "New Mexico Lobos", "FIU Panthers",
    "Pittsburgh Panthers", "Clemson Tigers", "UConn Huskies", "Georgia Tech Yellow Jackets", "Miami (OH) RedHawks",
    "San Diego State Aztecs", "Missouri Tigers", "LSU Tigers", "Appalachian State Mountaineers",
    "Coastal Carolina Chanticleers", "Tennessee Volunteers", "USC Trojans", "Vanderbilt Commodores", "Arizona State Sun Devils",
    "Michigan Wolverines", "Nebraska Cornhuskers", "Rice Owls", "Cincinnati Bearcats", "Mississippi State Bulldogs", "Arizona Wildcats",
    # CFP losers (round 1, quarterfinal, semifinal, championship)
    "Oklahoma Sooners", "Texas A&M Aggies", "Tulane Green Wave", "James Madison Dukes", "Ohio State Buckeyes",
    "Texas Tech Red Raiders", "Alabama Crimson Tide", "Georgia Bulldogs", "Ole Miss Rebels", "Oregon Ducks", "Miami (FL) Hurricanes",
}


def ncaaf_stats(name: str) -> dict:
    wins, total_losses = NCAAF_RECORDS[name]
    reg_season_losses = total_losses - (1 if name in NCAAF_BOWL_LOSERS else 0)
    return {
        "wins": wins,
        "reg_season_losses": reg_season_losses,
        "playoff_bid": name in NCAAF_PLAYOFF_BID,
        "playoff_wins": NCAAF_PLAYOFF_WINS.get(name, 0),
        "championship_bid": name in NCAAF_CHAMPIONSHIP_BID,
        "championship_win": name == NCAAF_CHAMPIONSHIP_WINNER,
    }


# ---------------------------------------------------------------------------
# NCAAMB 2025-26 — Michigan national champions. SCOPE: only the 16 teams that
# reached the Sweet 16 or better in the 2026 NCAA tournament are populated
# (not the ~360-team pool). For those 16: seed, final win-loss record
# (regular season + tournament games), and round-by-round tournament
# progress. `reg_season_conf_champ` and `conf_tourney_champ` are explicitly
# SKIPPED (left False for everyone) — identifying every conference's
# regular-season and tournament champion across ~31 conferences was out of
# scope; only the round-of-64-qualifier-onward bonuses are populated.
# ---------------------------------------------------------------------------

# name: (wins, losses, seed, furthest round reached)
# furthest round reached is one of: "sweet16" (lost Sweet 16), "elite8"
# (lost Elite Eight), "final4" (lost national semifinal), "runnerup" (lost
# championship game), "champion".
NCAAMB_RESULTS = {
    "Michigan Wolverines": (31, 3, 1, "champion"),
    "UConn Huskies": (29, 7, 2, "runnerup"),
    "Arizona Wildcats": (30, 5, 1, "final4"),
    "Illinois Fighting Illini": (26, 9, 3, "final4"),
    "Duke Blue Devils": (30, 4, 1, "elite8"),
    "Iowa State Cyclones": (26, 8, 2, "elite8"),
    "High Point Panthers": (30, 3, 12, "elite8"),
    "Houston Cougars": (27, 7, 2, "elite8"),
    "St. John's Red Storm": (26, 9, 5, "sweet16"),
    "Kansas Jayhawks": (23, 11, 4, "sweet16"),
    "Virginia Cavaliers": (27, 6, 3, "sweet16"),
    "Miami (OH) RedHawks": (29, 2, 11, "sweet16"),
    "Gonzaga Bulldogs": (28, 4, 3, "sweet16"),
    "Arkansas Razorbacks": (24, 9, 4, "sweet16"),
    "Nebraska Cornhuskers": (24, 7, 4, "sweet16"),
    "Iowa Hawkeyes": (19, 13, 9, "sweet16"),
}

# ---------------------------------------------------------------------------
# NCAAWB 2025-26 — UCLA national champions (their first title). Same scope
# limits as NCAAMB above: Sweet-16-or-better only (16 teams), and
# `reg_season_conf_champ` / `conf_tourney_champ` left False for everyone.
# ---------------------------------------------------------------------------

NCAAWB_RESULTS = {
    "UCLA Bruins": (37, 1, 1, "champion"),
    "South Carolina Gamecocks": (36, 4, 1, "runnerup"),
    "UConn Huskies": (38, 1, 1, "final4"),
    "Texas Longhorns": (35, 4, 1, "final4"),
    "Notre Dame Fighting Irish": (25, 11, 6, "elite8"),
    "Duke Blue Devils": (29, 9, 3, "elite8"),
    "Michigan Wolverines": (28, 7, 2, "elite8"),
    "TCU Horned Frogs": (32, 6, 3, "elite8"),
    "Louisville Cardinals": (29, 8, 3, "sweet16"),
    "West Virginia Mountaineers": (29, 7, 4, "sweet16"),
    "Oklahoma Sooners": (26, 8, 4, "sweet16"),
    "Virginia Cavaliers": (21, 12, 10, "sweet16"),
    "Vanderbilt Commodores": (29, 5, 2, "sweet16"),
    "Ohio State Buckeyes": (28, 8, 3, "sweet16"),
    "Minnesota Golden Gophers": (24, 9, 4, "sweet16"),
    "LSU Tigers": (29, 6, 2, "sweet16"),
}

_CBB_ROUND_LEVELS = {
    "sweet16": 2,
    "elite8": 3,
    "final4": 4,
    "runnerup": 5,
    "champion": 6,
}


def _cbb_stats(results: dict, name: str) -> dict:
    wins, losses, seed, round_reached = results[name]
    level = _CBB_ROUND_LEVELS[round_reached]
    return {
        "wins": wins,
        "losses": losses,
        "reg_season_conf_champ": False,  # out of scope — see module docstring
        "conf_tourney_champ": False,  # out of scope — see module docstring
        "ncaa_qualifier": True,
        "seed_1": seed == 1,
        "seed_2": seed == 2,
        "won_round_of_64": level >= 1,
        "won_round_of_32": level >= 1,  # reaching Sweet 16 implies both wins
        "won_sweet_16": level >= 2,
        "won_elite_8": level >= 3,
        "won_final_4": level >= 4,
        "won_championship": level >= 6,
    }


def ncaamb_stats(name: str) -> dict:
    return _cbb_stats(NCAAMB_RESULTS, name)


def ncaawb_stats(name: str) -> dict:
    return _cbb_stats(NCAAWB_RESULTS, name)


# ---------------------------------------------------------------------------
# ATP 2025 — men's tennis, 4 majors (Australian Open, French Open, Wimbledon,
# US Open; 2025 is the most recently completed calendar year with all 4
# done, since 2026's US Open hadn't happened yet as of this writing). SCOPE:
# only quarterfinal-round-onward results, aggregated by country, per the
# task's explicit limitation — `round_1_wins` through `round_4_wins` are
# left at 0 for every country (not researched). A country's
# `quarterfinal_wins` counts how many of its players won their QF (became a
# semifinalist) across all 4 majors combined; `semifinal_wins` similarly
# counts SF wins (became a finalist); `final_wins` counts final wins
# (became champion). Only 6 countries had any quarterfinalist across these
# 4 majors' analyzed rounds (the same handful of players dominated all
# four) — every other ATP_TEAMS country gets no row.
# ---------------------------------------------------------------------------

# country: (quarterfinal_wins, semifinal_wins, final_wins) summed across the
# 2025 Australian Open, French Open, Wimbledon, and US Open.
ATP_MAJORS_RESULTS = {
    "Italy": (5, 4, 2),           # Sinner: won AO, W; runner-up FO, USO
    "United States": (2, 0, 0),   # Shelton (AO QF->SF), Fritz (Wimbledon QF->SF)
    "Germany": (1, 1, 0),         # Zverev: AO runner-up
    "Serbia": (4, 0, 0),          # Djokovic: QF->SF at all 4 majors, no finals
    "Spain": (3, 3, 2),           # Alcaraz: won FO, USO; runner-up W
    "Canada": (1, 0, 0),          # Auger-Aliassime (USO QF->SF)
}

# ---------------------------------------------------------------------------
# WTA 2025 — women's tennis, same 4 majors and same QF-onward-only scope as
# ATP above (round_1_wins..round_4_wins left at 0 for every country).
# ---------------------------------------------------------------------------

WTA_MAJORS_RESULTS = {
    "United States": (4, 4, 2),    # Keys (won AO), Gauff (won FO), Anisimova (W/USO runner-up)
    "Poland": (4, 1, 1),           # Swiatek: won W, SF/QF at others
    "Belarus": (4, 3, 1),          # Sabalenka: won USO, runner-up AO/FO
    "Spain": (1, 0, 0),            # Badosa (AO QF->SF)
    "France": (1, 0, 0),           # Boisson (FO QF->SF)
    "Switzerland": (1, 0, 0),      # Bencic (Wimbledon QF->SF)
    "Czech Republic": (1, 0, 0),   # Muchova (USO QF->SF)
}


def _tennis_stats(results: dict, name: str) -> dict:
    qf, sf, fin = results[name]
    return {
        "round_1_wins": 0,  # out of scope — see module docstring
        "round_2_wins": 0,  # out of scope
        "round_3_wins": 0,  # out of scope
        "round_4_wins": 0,  # out of scope
        "quarterfinal_wins": qf,
        "semifinal_wins": sf,
        "final_wins": fin,
    }


def atp_stats(name: str) -> dict:
    return _tennis_stats(ATP_MAJORS_RESULTS, name)


def wta_stats(name: str) -> dict:
    return _tennis_stats(WTA_MAJORS_RESULTS, name)


# ---------------------------------------------------------------------------
# PGA 2026 — men's golf, all 4 majors (Masters, PGA Championship, U.S. Open,
# The Open Championship), aggregated by the starting letter of each
# player's last name. Sourced from each major's Wikipedia results table,
# generally down to ~T30/the cut line. Every letter's numbers below are the
# sum, across all 4 majors, of every player in the researched leaderboards
# whose last name starts with that letter: `made_cut_count` (1 per
# appearance in a final leaderboard) plus a placement-band count for
# whichever band their (possibly tied) finishing position falls into.
# Letters with no player in any researched leaderboard (O, Q, U, V, X, Z)
# get no row.
# ---------------------------------------------------------------------------

PGA_LETTER_STATS = {
    "A": {"made_cut_count": 4, "place_4_count": 1, "place_9_count": 1, "place_16_20_count": 1, "place_21_30_count": 1},
    "B": {"made_cut_count": 7, "place_2_count": 1, "place_3_count": 1, "place_7_count": 1, "place_16_20_count": 2, "place_21_30_count": 2},
    "C": {"made_cut_count": 9, "place_1_count": 1, "place_11_15_count": 2, "place_16_20_count": 1, "place_21_30_count": 6},
    "D": {"made_cut_count": 2, "place_11_15_count": 2},
    "E": {"made_cut_count": 2, "place_16_20_count": 1, "place_21_30_count": 1},
    "F": {"made_cut_count": 9, "place_1_count": 1, "place_4_count": 1, "place_11_15_count": 2, "place_16_20_count": 2, "place_21_30_count": 3},
    "G": {"made_cut_count": 8, "place_9_count": 1, "place_10_count": 1, "place_11_15_count": 2, "place_16_20_count": 2, "place_21_30_count": 2},
    "H": {"made_cut_count": 8, "place_3_count": 2, "place_6_count": 1, "place_7_count": 1, "place_9_count": 2, "place_16_20_count": 2},
    "I": {"made_cut_count": 1, "place_11_15_count": 1},
    "J": {"made_cut_count": 3, "place_6_count": 1, "place_16_20_count": 1, "place_21_30_count": 1},
    "K": {"made_cut_count": 6, "place_3_count": 1, "place_6_count": 1, "place_10_count": 1, "place_11_15_count": 2, "place_21_30_count": 1},
    "L": {"made_cut_count": 2, "place_16_20_count": 1, "place_21_30_count": 1},
    "M": {"made_cut_count": 11, "place_1_count": 1, "place_4_count": 1, "place_7_count": 2, "place_11_15_count": 2, "place_16_20_count": 4, "place_21_30_count": 1},
    "N": {"made_cut_count": 5, "place_7_count": 1, "place_9_count": 1, "place_16_20_count": 2, "place_21_30_count": 1},
    "P": {"made_cut_count": 4, "place_4_count": 1, "place_11_15_count": 1, "place_16_20_count": 2},
    "R": {"made_cut_count": 9, "place_1_count": 1, "place_2_count": 1, "place_3_count": 1, "place_10_count": 2, "place_11_15_count": 4, "place_16_20_count": 1},
    "S": {"made_cut_count": 18, "place_2_count": 2, "place_4_count": 3, "place_7_count": 3, "place_9_count": 2, "place_11_15_count": 3, "place_16_20_count": 3, "place_21_30_count": 2},
    "T": {"made_cut_count": 3, "place_4_count": 1, "place_11_15_count": 1, "place_16_20_count": 1},
    "W": {"made_cut_count": 1, "place_7_count": 1},
    "Y": {"made_cut_count": 2, "place_2_count": 1, "place_3_count": 1},
}

# ---------------------------------------------------------------------------
# LPGA 2026 — women's golf, the 4 *counted* majors per the wiki (Chevron
# Championship, U.S. Women's Open, KPMG Women's PGA Championship, AIG
# Women's Open — the Evian Championship is deliberately excluded, same as
# the roster rules). Same letter-aggregation approach as PGA above.
# Depth varies significantly by major and is a documented limitation: the
# Chevron and AIG Women's Open leaderboards found only went ~10-11 players
# deep, U.S. Women's Open ~14 deep, but KPMG's leaderboard was available
# nearly full-field (~69 players) — so KPMG contributes made-cut counts for
# players well outside any placement band (position >30, no placement bonus,
# made_cut_count only) alongside the shallower events' top-of-leaderboard
# placement bands. Letters with no player in any researched leaderboard
# (E, Q, U, V, X) get no row.
# ---------------------------------------------------------------------------

LPGA_LETTER_STATS = {
    "A": {"made_cut_count": 2, "place_8_count": 1},
    "B": {"made_cut_count": 2},
    "C": {"made_cut_count": 8, "place_4_count": 1, "place_5_count": 1, "place_8_count": 1, "place_21_30_count": 3},
    "D": {"made_cut_count": 3, "place_11_15_count": 1, "place_21_30_count": 1},
    "F": {"made_cut_count": 3, "place_16_20_count": 1},
    "G": {"made_cut_count": 2, "place_7_count": 1, "place_21_30_count": 1},
    "H": {"made_cut_count": 10, "place_2_count": 2, "place_3_count": 1, "place_6_count": 3, "place_10_count": 1, "place_11_15_count": 2},
    "I": {"made_cut_count": 1, "place_16_20_count": 1},
    "J": {"made_cut_count": 1},
    "K": {"made_cut_count": 20, "place_1_count": 3, "place_4_count": 1, "place_5_count": 2, "place_6_count": 1, "place_8_count": 4, "place_11_15_count": 1, "place_21_30_count": 3},
    "L": {"made_cut_count": 9, "place_2_count": 1, "place_4_count": 1, "place_5_count": 1, "place_11_15_count": 1, "place_16_20_count": 2},
    "M": {"made_cut_count": 4, "place_8_count": 1},
    "N": {"made_cut_count": 3, "place_3_count": 1},
    "O": {"made_cut_count": 1, "place_8_count": 1},
    "P": {"made_cut_count": 4, "place_16_20_count": 1},
    "R": {"made_cut_count": 4, "place_1_count": 1, "place_6_count": 2},
    "S": {"made_cut_count": 5, "place_8_count": 1},
    "T": {"made_cut_count": 7, "place_2_count": 1, "place_4_count": 1, "place_6_count": 2, "place_8_count": 1},
    "W": {"made_cut_count": 3, "place_3_count": 1, "place_6_count": 1, "place_9_count": 1},
    "Y": {"made_cut_count": 9, "place_2_count": 1, "place_3_count": 1, "place_5_count": 1, "place_8_count": 1, "place_11_15_count": 2, "place_16_20_count": 1},
    "Z": {"made_cut_count": 2},
}


def pga_stats(name: str) -> dict:
    return PGA_LETTER_STATS[name]


def lpga_stats(name: str) -> dict:
    return LPGA_LETTER_STATS[name]


# ---------------------------------------------------------------------------
# F1 2025 — the 10 constructors that competed that season (Cadillac is a new
# 2026 entrant with no 2025 result; Sauber's works team is keyed here as
# "Audi" to match the current Team.name post-rebrand, same idea as NHL's
# Utah Mammoth keying for a renamed/relocated franchise).
#
# wins/podiums/poles/fastest_laps are EXACT, cross-checked against the race-
# by-race winner list, pole-position list, and per-driver podium/fastest-lap
# tallies (Formula1.com official results, gpracingstats.com, 4mula1stats.com)
# — each column's per-team sum reconciles against the known season totals
# (24 wins, 72 podiums, 24 poles, 24 fastest laps across 24 races).
# points_finishes/non_points_finishes and the sprint breakdown are REASONED
# ESTIMATES (a team's known podium count plus an estimated share of the
# remaining P4-P10/sprint-top-8 finishes, proportional to its competitive
# tier that season) rather than a full race-by-race classification pull for
# all 480 car-race entries — the same kind of documented scope trade-off as
# NCAAF's bowl-loss coverage or NHL's OT-win split elsewhere in this file.
F1_CONSTRUCTOR_STATS = {
    # (points_finishes, non_points_finishes, podiums, wins, poles, fastest_laps,
    #  sprint_points_finishes, sprint_podiums, sprint_wins, championship_place)
    "McLaren": (44, 4, 34, 14, 13, 12, 11, 8, 3, 1),
    "Mercedes": (38, 10, 12, 2, 2, 6, 9, 3, 0, 2),
    "Red Bull Racing": (33, 15, 15, 8, 8, 3, 8, 4, 2, 3),
    "Ferrari": (34, 14, 7, 0, 1, 2, 9, 2, 1, None),
    "Williams": (24, 24, 2, 0, 0, 1, 6, 1, 0, None),
    "Aston Martin": (17, 31, 0, 0, 0, 0, 4, 0, 0, None),
    "Racing Bulls": (16, 32, 1, 0, 0, 0, 4, 0, 0, None),
    "Haas": (15, 33, 0, 0, 0, 0, 4, 0, 0, None),
    "Audi": (14, 34, 1, 0, 0, 0, 3, 0, 0, None),
    "Alpine": (5, 43, 0, 0, 0, 0, 1, 0, 0, None),
}


def f1_stats(name: str) -> dict:
    (
        points_finishes, non_points_finishes, podiums, wins, poles, fastest_laps,
        sprint_points_finishes, sprint_podiums, sprint_wins, championship_place,
    ) = F1_CONSTRUCTOR_STATS[name]
    return {
        "points_finishes": points_finishes,
        "non_points_finishes": non_points_finishes,
        "podiums": podiums,
        "wins": wins,
        "poles": poles,
        "fastest_laps": fastest_laps,
        "sprint_points_finishes": sprint_points_finishes,
        "sprint_podiums": sprint_podiums,
        "sprint_wins": sprint_wins,
        "championship_place": championship_place,
    }


# ---------------------------------------------------------------------------
# WNBA 2025 — regular season records, top-8 playoff bracket (Aces
# champions). Portland Fire and Toronto Tempo are brand-new 2026 expansion
# franchises (added via an April 2026 expansion draft) with no 2025 result
# — same treatment as F1's Cadillac above; they simply aren't keys in
# WNBA_RECORDS, so seed()'s generic loop skips them automatically.
WNBA_RECORDS = {
    "Minnesota Lynx": (34, 10), "Las Vegas Aces": (30, 14), "Atlanta Dream": (30, 14),
    "Phoenix Mercury": (27, 17), "New York Liberty": (27, 17), "Indiana Fever": (24, 20),
    "Seattle Storm": (23, 21), "Golden State Valkyries": (23, 21),
    "Los Angeles Sparks": (21, 23), "Washington Mystics": (16, 28),
    "Connecticut Sun": (11, 33), "Chicago Sky": (10, 34), "Dallas Wings": (10, 34),
}
WNBA_MADE_PLAYOFFS = {
    "Minnesota Lynx", "Las Vegas Aces", "Atlanta Dream", "Phoenix Mercury",
    "New York Liberty", "Indiana Fever", "Seattle Storm", "Golden State Valkyries",
}
# Round 1 (best-of-3): Lynx def. Valkyries 2-0, Aces def. Storm 2-1,
# Fever def. Dream 2-1, Mercury def. Liberty 2-1
WNBA_ROUND1_WINNERS = {"Minnesota Lynx", "Las Vegas Aces", "Indiana Fever", "Phoenix Mercury"}
# Semifinals (best-of-5): Mercury def. Lynx 3-1, Aces def. Fever 3-2 (OT Game 5)
WNBA_SEMIS_WINNERS = {"Phoenix Mercury", "Las Vegas Aces"}
# Finals (best-of-7, new format as of 2025): Aces def. Mercury 4-0
WNBA_CHAMPION = "Las Vegas Aces"


def wnba_stats(name: str) -> dict:
    wins, losses = WNBA_RECORDS[name]
    return {
        "wins": wins,
        "losses": losses,
        "made_playoffs": name in WNBA_MADE_PLAYOFFS,
        "won_round1": name in WNBA_ROUND1_WINNERS,
        "won_semis": name in WNBA_SEMIS_WINNERS,
        "won_wnba_champ": name == WNBA_CHAMPION,
    }


# ---------------------------------------------------------------------------
# MLS 2025 — final regular-season points/GD (old Feb/March-Dec calendar;
# the league doesn't switch to the July-May calendar this formula was
# designed for until 2027, so 2025 is still the most recently completed
# season as of this writing), full playoff bracket (Inter Miami champions).
MLS_TABLE = {
    # (points, goal_differential) — Eastern Conference
    "Philadelphia Union": (66, 22), "FC Cincinnati": (65, 12), "Inter Miami CF": (65, 26),
    "Charlotte FC": (59, 9), "New York City FC": (56, 6), "Nashville SC": (54, 13),
    "Columbus Crew": (54, 4), "Chicago Fire FC": (53, 8), "Orlando City SC": (53, 12),
    "New York Red Bulls": (43, 1), "New England Revolution": (36, -7), "Toronto FC": (32, -7),
    "CF Montréal": (28, -26), "Atlanta United FC": (28, -25), "D.C. United": (26, -36),
    # Western Conference
    "San Diego FC": (63, 23), "Vancouver Whitecaps FC": (63, 28), "Los Angeles FC": (60, 25),
    "Minnesota United FC": (58, 17), "Seattle Sounders FC": (55, 10), "Austin FC": (47, -8),
    "FC Dallas": (44, -3), "Portland Timbers": (44, -7), "Real Salt Lake": (41, -11),
    "San Jose Earthquakes": (41, -3), "Colorado Rapids": (41, -12), "Houston Dynamo FC": (37, -13),
    "St. Louis City SC": (32, -14), "LA Galaxy": (30, -20), "Sporting Kansas City": (28, -24),
}
MLS_SHIELD_WINNER = "Philadelphia Union"
# Top 9 of 15 in each conference qualify (18 total); seeds 8-9 play a Wild
# Card game first, but that's collapsed into a single "made the playoffs"
# flag here rather than tracked separately.
MLS_MADE_PLAYOFFS = {
    "Philadelphia Union", "FC Cincinnati", "Inter Miami CF", "Charlotte FC",
    "New York City FC", "Nashville SC", "Columbus Crew", "Chicago Fire FC", "Orlando City SC",
    "San Diego FC", "Vancouver Whitecaps FC", "Los Angeles FC", "Minnesota United FC",
    "Seattle Sounders FC", "Austin FC", "FC Dallas", "Portland Timbers", "Real Salt Lake",
}
# Won Round One best-of-3 (reached Conference Semifinals)
MLS_ROUND1_WINNERS = {
    "Inter Miami CF", "FC Cincinnati", "New York City FC", "Philadelphia Union",
    "San Diego FC", "Minnesota United FC", "Vancouver Whitecaps FC", "Los Angeles FC",
}
# Won Conference Semifinal (reached Conference Final)
MLS_CONF_SEMI_WINNERS = {"Inter Miami CF", "New York City FC", "Vancouver Whitecaps FC", "San Diego FC"}
# Won Conference Final (reached MLS Cup)
MLS_CONF_FINAL_WINNERS = {"Inter Miami CF", "Vancouver Whitecaps FC"}
MLS_CUP_WINNER = "Inter Miami CF"


def mls_stats(name: str) -> dict:
    points, gd = MLS_TABLE[name]
    return {
        "standings_points": points,
        "goal_differential": gd,
        "won_shield": name == MLS_SHIELD_WINNER,
        "made_playoffs": name in MLS_MADE_PLAYOFFS,
        "won_round1": name in MLS_ROUND1_WINNERS,
        "won_conf_semi": name in MLS_CONF_SEMI_WINNERS,
        "won_conf_final": name in MLS_CONF_FINAL_WINNERS,
        "won_mls_cup": name == MLS_CUP_WINNER,
    }


# ---------------------------------------------------------------------------
# NWSL 2025 — final regular-season table (points, goal differential) for all
# 14 teams that existed that season, plus the full playoff bracket. Directly
# sourced, no scoping gaps. Boston Legacy FC and Denver Summit FC are
# brand-new 2026 expansion franchises with no 2025 history, so they aren't
# keyed here — same treatment as this app's other mid-cycle expansion teams.
NWSL_TABLE = {
    # (wins, draws, losses, goal_differential, standings_points)
    "Kansas City Current": (21, 2, 3, 36, 65),
    "Washington Spirit": (12, 8, 6, 9, 44),
    "Portland Thorns FC": (11, 7, 8, 7, 40),
    "Orlando Pride": (11, 7, 8, 6, 40),
    "Seattle Reign FC": (10, 9, 7, 3, 39),
    "San Diego Wave FC": (10, 7, 9, 7, 37),
    "Racing Louisville FC": (10, 7, 9, -3, 37),
    "Gotham FC": (9, 9, 8, 10, 36),
    "North Carolina Courage": (9, 8, 9, -2, 35),
    "Houston Dash": (8, 6, 12, -12, 30),
    "Angel City FC": (7, 6, 13, -10, 27),
    "Utah Royals": (6, 7, 13, -14, 25),
    "Bay FC": (4, 8, 14, -15, 20),
    "Chicago Stars FC": (3, 11, 12, -22, 20),
}
NWSL_SHIELD_WINNER = "Kansas City Current"
NWSL_MADE_PLAYOFFS = {
    "Kansas City Current", "Washington Spirit", "Portland Thorns FC", "Orlando Pride",
    "Seattle Reign FC", "San Diego Wave FC", "Racing Louisville FC", "Gotham FC",
}
# Quarterfinals: Orlando bt Seattle, Washington bt Racing Louisville (on
# penalties), Gotham bt Kansas City, Portland bt San Diego (after extra time)
NWSL_QUARTERFINAL_WINNERS = {"Orlando Pride", "Washington Spirit", "Gotham FC", "Portland Thorns FC"}
# Semifinals: Washington bt Portland, Gotham bt Orlando
NWSL_SEMIFINAL_WINNERS = {"Washington Spirit", "Gotham FC"}
# Championship (Nov 22, 2025): Gotham FC bt Washington Spirit 1-0 — the
# lowest seed (No. 8) ever to win the title
NWSL_CHAMPION = "Gotham FC"


def nwsl_stats(name: str) -> dict:
    wins, draws, losses, goal_differential, standings_points = NWSL_TABLE[name]
    return {
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "goal_differential": goal_differential,
        "standings_points": standings_points,
        "won_shield": name == NWSL_SHIELD_WINNER,
        "made_playoffs": name in NWSL_MADE_PLAYOFFS,
        "won_quarterfinal": name in NWSL_QUARTERFINAL_WINNERS,
        "won_semifinal": name in NWSL_SEMIFINAL_WINNERS,
        "won_championship": name == NWSL_CHAMPION,
    }


# ---------------------------------------------------------------------------
# Tour de France Team Classification, 2026 edition — the most recently
# completed real Tour as of this writing (2027's isn't run until next July).
# Only the top 3 are backfilled here (Lidl-Trek won by 36:57 over UAE Team
# Emirates XRG, with Red Bull-BORA-Hansgrohe 3rd at +1:06:22) — the source
# used for this only reported the full final classification through 3rd,
# not all 23 teams, so the rest are deliberately left without a historical
# row rather than guessing a placement (same principle as any team this app
# doesn't have a confidently-sourced result for).
TDF_TEAM_PLACE = {
    "Lidl–Trek": 1,
    "UAE Team Emirates XRG": 2,
    "Red Bull–Bora–Hansgrohe": 3,
}


def tdf_stats(name: str) -> dict:
    return {"place": TDF_TEAM_PLACE[name]}


# ---------------------------------------------------------------------------
# URC 2025-26 — final regular-season table (points, points difference) for
# all 16 clubs, full playoff bracket (Leinster champions, beat the Bulls
# 36-7 in the Grand Final — a repeat of the 2025 final — for a 2nd
# consecutive title and a record 10th overall). This is the most recently
# completed real season as of this writing (Grand Final June 19, 2026);
# supersedes the 2024-25 data this app briefly carried after the in-story
# clock passed that season's completion without the historical backfill
# being refreshed to match. Directly sourced, no scoping gaps — full
# 16-team pool, no scale problem like NCAAMB/tennis.
URC_TABLE = {
    # (table_points, points_difference)
    "Glasgow Warriors": (65, 141), "Leinster": (63, 145), "Stormers": (60, 160), "Bulls": (59, 170),
    "Munster": (55, 20), "Cardiff": (55, -19), "Lions": (54, 59), "Connacht": (54, 47),
    "Ulster": (52, 74), "Sharks": (46, 39), "Ospreys": (39, -78), "Edinburgh": (38, -77),
    "Benetton": (33, -166), "Scarlets": (28, -99), "Dragons": (28, -131), "Zebre Parma": (15, -275),
}
URC_MADE_PLAYOFFS = {
    "Glasgow Warriors", "Leinster", "Stormers", "Bulls",
    "Munster", "Cardiff", "Lions", "Connacht",
}
# Quarterfinals: Leinster bt Lions 59-10, Bulls bt Munster 45-14, Stormers
# bt Cardiff 44-21, Glasgow bt Connacht
URC_QUARTERFINAL_WINNERS = {"Leinster", "Bulls", "Stormers", "Glasgow Warriors"}
# Semifinals: Bulls bt Glasgow 22-21 (from 21-3 down), Leinster bt Stormers 20-11
URC_SEMIFINAL_WINNERS = {"Bulls", "Leinster"}
URC_FINAL_WINNER = "Leinster"


def urc_stats(name: str) -> dict:
    table_points, points_difference = URC_TABLE[name]
    return {
        "table_points": table_points,
        "points_difference": points_difference,
        "made_playoffs": name in URC_MADE_PLAYOFFS,
        "won_quarterfinal": name in URC_QUARTERFINAL_WINNERS,
        "won_semifinal": name in URC_SEMIFINAL_WINNERS,
        "won_final": name == URC_FINAL_WINNER,
    }


# ---------------------------------------------------------------------------
# IPL 2026 — final points table (Royal Challengers Bengaluru back-to-back
# champions, beat Gujarat Titans in the Final). Unlike every other spring
# league above, IPL 2026 (March 28 - May 31, 2026) is already the most
# recently COMPLETED season as of this writing, not 2025 — the season
# starts and finishes entirely within a single calendar year, and 2026's
# already wrapped up. Directly sourced, all 10 teams, no scoping gaps.
IPL_TABLE = {
    # (wins, losses, ties, net_run_rate)
    "Royal Challengers Bengaluru": (9, 5, 0, 0.783),
    "Gujarat Titans": (9, 5, 0, 0.695),
    "Sunrisers Hyderabad": (9, 5, 0, 0.524),
    "Rajasthan Royals": (8, 6, 0, 0.189),
    "Punjab Kings": (7, 6, 1, 0.309),
    "Delhi Capitals": (7, 7, 0, -0.651),
    "Kolkata Knight Riders": (6, 7, 1, -0.147),
    "Chennai Super Kings": (6, 8, 0, -0.345),
    "Mumbai Indians": (4, 10, 0, -0.584),
    "Lucknow Super Giants": (4, 10, 0, -0.740),
}
IPL_MADE_PLAYOFFS = {
    "Royal Challengers Bengaluru", "Gujarat Titans", "Sunrisers Hyderabad", "Rajasthan Royals",
}
# IPL's knockout stage is a "page playoff," not a clean bracket: Qualifier 1
# (1st vs 2nd, winner goes straight to the Final), Eliminator (3rd vs 4th,
# loser is out), Qualifier 2 (Q1 loser vs Eliminator winner, winner reaches
# the Final). 2026: RCB beat GT in Q1 (RCB straight to Final); RR beat SRH
# in the Eliminator; GT beat RR in Q2 (GT reaches the Final via the back
# door). Final: RCB beat GT.
IPL_KNOCKOUT_WINS = {
    "Royal Challengers Bengaluru": 1,  # won Q1
    "Gujarat Titans": 1,  # lost Q1, won Q2
    "Rajasthan Royals": 1,  # won the Eliminator, lost Q2
    "Sunrisers Hyderabad": 0,  # lost the Eliminator
}
IPL_FINALISTS = {"Royal Challengers Bengaluru", "Gujarat Titans"}
IPL_CHAMPION = "Royal Challengers Bengaluru"


def ipl_stats(name: str) -> dict:
    wins, losses, ties, net_run_rate = IPL_TABLE[name]
    return {
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "net_run_rate": net_run_rate,
        "made_playoffs": name in IPL_MADE_PLAYOFFS,
        "knockout_wins": IPL_KNOCKOUT_WINS.get(name, 0),
        "reached_final": name in IPL_FINALISTS,
        "won_final": name == IPL_CHAMPION,
    }


# ---------------------------------------------------------------------------

LEAGUE_SEASONS = [
    ("MLB", "2025", MLB_RECORDS, mlb_stats),
    ("NFL", "2025", NFL_RECORDS, nfl_stats),
    ("NBA", "2025-26", NBA_RECORDS, nba_stats),
    ("NHL", "2025-26", NHL_RECORDS, nhl_stats),
    ("EPL", "2025-26", EPL_TABLE, epl_stats),
    ("NCAAF", "2025", NCAAF_RECORDS, ncaaf_stats),
    ("NCAAMB", "2025-26", NCAAMB_RESULTS, ncaamb_stats),
    ("NCAAWB", "2025-26", NCAAWB_RESULTS, ncaawb_stats),
    ("ATP", "2025", ATP_MAJORS_RESULTS, atp_stats),
    ("WTA", "2025", WTA_MAJORS_RESULTS, wta_stats),
    ("PGA", "2026", PGA_LETTER_STATS, pga_stats),
    ("LPGA", "2026", LPGA_LETTER_STATS, lpga_stats),
    ("F1", "2025", F1_CONSTRUCTOR_STATS, f1_stats),
    ("WNBA", "2025", WNBA_RECORDS, wnba_stats),
    ("MLS", "2025", MLS_TABLE, mls_stats),
    ("URC", "2025-26", URC_TABLE, urc_stats),
    ("IPL", "2026", IPL_TABLE, ipl_stats),
    ("NWSL", "2025", NWSL_TABLE, nwsl_stats),
    ("TDF", "2026", TDF_TEAM_PLACE, tdf_stats),
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        added = 0
        skipped_no_team = []
        for league, season_label, names_map, stats_fn in LEAGUE_SEASONS:
            for name in names_map:
                team = db.query(Team).filter(Team.league == league, Team.name == name).first()
                if team is None:
                    # EPL's prior-season table includes West Ham/Burnley/Wolves,
                    # who were relegated and aren't in the current Team table
                    # (which reflects the *current* 2026/27 season's clubs).
                    skipped_no_team.append(f"{league} {name}")
                    continue

                existing = (
                    db.query(TeamSeasonResult)
                    .filter(TeamSeasonResult.team_id == team.id, TeamSeasonResult.season_label == season_label)
                    .first()
                )
                stats = stats_fn(name)
                if existing:
                    existing.stats = stats
                else:
                    db.add(
                        TeamSeasonResult(
                            team_id=team.id,
                            league=league,
                            season_label=season_label,
                            stats=stats,
                        )
                    )
                    added += 1
        db.commit()

        print(f"Added/updated {added} team-season results.")
        if skipped_no_team:
            print(
                f"Skipped {len(skipped_no_team)} teams not in the current Team table "
                f"(e.g. relegated EPL clubs): {', '.join(skipped_no_team)}"
            )
    finally:
        db.close()


if __name__ == "__main__":
    seed()
