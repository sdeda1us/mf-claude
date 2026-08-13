"""Single source of truth for roster limits and scoring rules.

Mirrors docs/wiki/game-rules-*.md — keep both in sync when rules change.
Playoff/round bonuses stack cumulatively (a champion also banks the
earlier-round bonuses). Per-game win/loss points apply to regular-season
games only for MLB/NFL/NBA/NHL/EPL — postseason success is captured solely
via the round bonuses there. NCAAF is the exception: its win/loss points
include bowl and playoff games too, with bowl/playoff losses scoring 0
instead of the usual -6 (see compute_score below).
"""

ROSTER_LIMITS: dict[str, int] = {
    "MLB": 4,
    "NFL": 4,
    "NBA": 4,
    "NHL": 4,
    "EPL": 2,
    "NCAAF": 5,
    "NCAAMB": 7,
    "NCAAWB": 7,
    "ATP": 2,
    "WTA": 2,
    "PGA": 3,
    "LPGA": 3,
    "F1": 1,
    "WNBA": 2,
    "MLS": 4,
    "URC": 2,
    "IPL": 1,
    "NWSL": 2,
    # Single-event classification (one Tour a year, one final ranking) —
    # capped at 1, same reasoning as F1/IPL's single-title caps.
    "TDF": 1,
}

# Which of the two auction sessions each league is drafted in — see
# docs/wiki/README.md's "Auction Sessions" section for why each league lands
# where it does.
LEAGUE_SESSION: dict[str, str] = {
    "EPL": "fall",
    "NCAAF": "fall",
    "NFL": "fall",
    "NHL": "fall",
    "NBA": "fall",
    "NCAAMB": "fall",
    "NCAAWB": "fall",
    "ATP": "fall",
    "WTA": "fall",
    "URC": "fall",
    "MLB": "spring",
    "PGA": "spring",
    "LPGA": "spring",
    "F1": "spring",
    "WNBA": "spring",
    "MLS": "spring",
    "IPL": "spring",
    "NWSL": "spring",
    "TDF": "spring",
}

# Some college leagues cap how many of a player's roster can come from a
# "minor" conference, on top of the ROSTER_LIMITS total above — enforced in
# auction_service.py / ws/auction_ws.py via is_minor_conference_team below.
MINOR_CONFERENCE_CAPS: dict[str, int] = {
    "NCAAF": 1,
    "NCAAMB": 2,
    "NCAAWB": 2,
}

# NCAAF roster rule: at most 1 of a player's 5 teams may come from a "minor"
# conference (Group of Five + non-Notre-Dame independents).
NCAAF_MINOR_CONFERENCE_TEAMS: set[str] = {
    # American
    "Army Black Knights", "Charlotte 49ers", "East Carolina Pirates", "Florida Atlantic Owls", "Memphis Tigers",
    "Navy Midshipmen", "North Texas Mean Green", "Rice Owls", "South Florida Bulls", "Temple Owls", "Tulane Green Wave",
    "Tulsa Golden Hurricane", "UAB Blazers", "UTSA Roadrunners",
    # Sun Belt
    "Appalachian State Mountaineers", "Arkansas State Red Wolves", "Coastal Carolina Chanticleers",
    "Georgia Southern Eagles", "Georgia State Panthers", "James Madison Dukes", "Louisiana Ragin' Cajuns",
    "Louisiana-Monroe Warhawks", "Louisiana Tech Bulldogs", "Marshall Thundering Herd", "Old Dominion Monarchs",
    "South Alabama Jaguars", "Southern Miss Golden Eagles", "Troy Trojans",
    # MAC
    "Akron Zips", "Ball State Cardinals", "Bowling Green Falcons", "Buffalo Bulls", "Central Michigan Chippewas",
    "Eastern Michigan Eagles", "Kent State Golden Flashes", "Miami (OH) RedHawks", "Ohio Bobcats",
    "Sacramento State Hornets", "Toledo Rockets", "UMass Minutemen", "Western Michigan Broncos",
    # Conference USA
    "Delaware Blue Hens", "FIU Panthers", "Jacksonville State Gamecocks", "Kennesaw State Owls", "Liberty Flames",
    "Middle Tennessee Blue Raiders", "Missouri State Bears", "New Mexico State Aggies", "Sam Houston Bearkats",
    "Western Kentucky Hilltoppers",
    # Mountain West
    "Air Force Falcons", "Hawaii Rainbow Warriors", "Nevada Wolf Pack", "New Mexico Lobos", "North Dakota State Bison",
    "Northern Illinois Huskies", "San Jose State Spartans", "UNLV Rebels", "UTEP Miners", "Wyoming Cowboys",
    # Pac-12
    "Boise State Broncos", "Colorado State Rams", "Fresno State Bulldogs", "Oregon State Beavers",
    "San Diego State Aztecs", "Texas State Bobcats", "Utah State Aggies", "Washington State Cougars",
    # Independent (minor)
    "UConn Huskies",
}

# NCAAMB/NCAAWB roster rule: at most 2 of a player's 7 teams may come from a
# "minor" conference. Major = SEC, Big Ten, ACC, Big 12, Big East (Notre
# Dame plays ACC basketball, UConn plays Big East basketball — no separate
# independent designation needed here, unlike NCAAF). Same major/minor
# split applies to both the men's and women's pools.
CBB_MAJOR_CONFERENCE_TEAMS: set[str] = {
    # SEC
    "Alabama Crimson Tide", "Arkansas Razorbacks", "Auburn Tigers", "Florida Gators", "Georgia Bulldogs", "Kentucky Wildcats", "LSU Tigers",
    "Ole Miss Rebels", "Mississippi State Bulldogs", "Missouri Tigers", "Oklahoma Sooners", "South Carolina Gamecocks",
    "Tennessee Volunteers", "Texas Longhorns", "Texas A&M Aggies", "Vanderbilt Commodores",
    # Big Ten
    "Illinois Fighting Illini", "Indiana Hoosiers", "Iowa Hawkeyes", "Maryland Terrapins", "Michigan Wolverines", "Michigan State Spartans",
    "Minnesota Golden Gophers", "Nebraska Cornhuskers", "Northwestern Wildcats", "Ohio State Buckeyes", "Oregon Ducks",
    "Penn State Nittany Lions", "Purdue Boilermakers", "Rutgers Scarlet Knights", "UCLA Bruins", "USC Trojans", "Washington Huskies", "Wisconsin Badgers",
    # ACC
    "Boston College Eagles", "California Golden Bears", "Clemson Tigers", "Duke Blue Devils", "Florida State Seminoles",
    "Georgia Tech Yellow Jackets", "Louisville Cardinals", "Miami (FL) Hurricanes", "North Carolina Tar Heels", "NC State Wolfpack",
    "Notre Dame Fighting Irish", "Pittsburgh Panthers", "SMU Mustangs", "Stanford Cardinal", "Syracuse Orange", "Virginia Cavaliers",
    "Virginia Tech Hokies", "Wake Forest Demon Deacons",
    # Big 12
    "Arizona Wildcats", "Arizona State Sun Devils", "Baylor Bears", "BYU Cougars", "Cincinnati Bearcats", "Colorado Buffaloes",
    "Houston Cougars", "Iowa State Cyclones", "Kansas Jayhawks", "Kansas State Wildcats", "Oklahoma State Cowboys",
    "TCU Horned Frogs", "Texas Tech Red Raiders", "UCF Knights", "Utah Utes", "West Virginia Mountaineers",
    # Big East
    "Butler Bulldogs", "UConn Huskies", "Creighton Bluejays", "DePaul Blue Demons", "Georgetown Hoyas", "Marquette Golden Eagles",
    "Providence Friars", "St. John's Red Storm", "Seton Hall Pirates", "Villanova Wildcats", "Xavier Musketeers",
}


def is_minor_conference_team(league: str, team_name: str) -> bool:
    if league == "NCAAF":
        return team_name in NCAAF_MINOR_CONFERENCE_TEAMS
    if league in ("NCAAMB", "NCAAWB"):
        return team_name not in CBB_MAJOR_CONFERENCE_TEAMS
    return False


# Shared by NCAAMB and NCAAWB — identical scoring rules for both.
CBB_SCORING_RULES: list[dict] = [
    {"label": "Win (regular season or conference tournament)", "points": 3},
    {"label": "Loss", "points": -1},
    {"label": "Regular-season conference champion (#1 seed in conf. tourney)", "points": 5},
    {"label": "Conference tournament champion", "points": 10},
    {"label": "NCAA Tournament qualifier", "points": 15},
    {"label": "— additional bonus if a #1 seed", "points": 10},
    {"label": "— additional bonus if a #2 seed", "points": 5},
    {"label": "Win Round of 64 (1st round)", "points": 5},
    {"label": "Win Round of 32 (2nd round)", "points": 5},
    {"label": "Win Sweet 16 (3rd round)", "points": 5},
    {"label": "Win Elite Eight (4th round)", "points": 10},
    {"label": "Win Final Four (5th round)", "points": 10},
    {"label": "Win National Championship", "points": 25},
]

# Shared by ATP and WTA. The "team" is a country: a country's score at a
# major sums every one of its players' round wins there (see compute_score).
TENNIS_SCORING_RULES: list[dict] = [
    {"label": "1st round win", "points": 2},
    {"label": "2nd round win", "points": 3},
    {"label": "3rd round win", "points": 5},
    {"label": "4th round win", "points": 5},
    {"label": "5th round win (quarterfinal)", "points": 7},
    {"label": "6th round win (semifinal)", "points": 8},
    {"label": "Final win (championship)", "points": 10},
]

# Shared by PGA and LPGA. The "team" is a letter of the alphabet: a
# letter's score at a major sums the scores of every player in that major's
# field whose last name starts with that letter. Placement bonuses are NOT
# cumulative with each other (a player finishes in exactly one place); the
# "makes the cut" bonus is separate and stacks additively on top.
GOLF_SCORING_RULES: list[dict] = [
    {"label": "Makes the cut", "points": 10},
    {"label": "Finishes 21st-30th", "points": 5},
    {"label": "Finishes 16th-20th", "points": 7},
    {"label": "Finishes 11th-15th", "points": 9},
    {"label": "Finishes 10th", "points": 10},
    {"label": "Finishes 9th", "points": 11},
    {"label": "Finishes 8th", "points": 12},
    {"label": "Finishes 7th", "points": 14},
    {"label": "Finishes 6th", "points": 16},
    {"label": "Finishes 5th", "points": 18},
    {"label": "Finishes 4th", "points": 20},
    {"label": "Finishes 3rd", "points": 25},
    {"label": "Finishes 2nd", "points": 35},
    {"label": "Wins", "points": 50},
]

# The "team" is a constructor (a works team fielding two cars) — stats
# combine both cars' results across the season. Calibrated against this
# app's other single-entity leagues (MLB/NFL/NBA/NHL/EPL/NCAAF), not the
# letter/country-aggregator leagues (PGA/LPGA/ATP/WTA), whose totals sum
# many real players and run far higher. A race win banks the points-finish,
# podium, and win bonuses simultaneously (cumulative, same convention as
# every other league here); sprint results are a separate counter set from
# main-race results, never double-counted; the championship bonus is a
# single flat bonus, exclusive across places.
F1_SCORING_RULES: list[dict] = [
    {"label": "Points finish (P1-P10, per car per race)", "points": 1},
    {"label": "Non-points finish or DNF (per car per race)", "points": -1},
    {"label": "— additional bonus if a podium (P1-P3)", "points": 3},
    {"label": "— additional bonus if a race win", "points": 5},
    {"label": "Pole position", "points": 2},
    {"label": "Fastest lap", "points": 1},
    {"label": "Sprint points finish (top 8, per car per sprint)", "points": 1},
    {"label": "— additional bonus if a sprint podium", "points": 1},
    {"label": "— additional bonus if a sprint win", "points": 2},
    {"label": "Constructors' Championship — 1st", "points": 30},
    {"label": "Constructors' Championship — 2nd", "points": 18},
    {"label": "Constructors' Championship — 3rd", "points": 10},
]

# EPL-style base (points + GD), like MLS/URC — NWSL, like WNBA, has used a
# single unified standings table (no conferences) since before this app's
# tracking window, with an 8-team single bracket (Quarterfinal, Semifinal,
# Championship — 3 rounds), so playoff bonuses reuse URC's 3-round scale.
# The NWSL Shield (best regular-season record) mirrors MLS's Supporters'
# Shield bonus.
NWSL_SCORING_RULES: list[dict] = [
    {"label": "Per point in the standings", "points": 2},
    {"label": "Per goal of goal differential (GD)", "points": 1},
    {"label": "Win the NWSL Shield (best regular-season record)", "points": 15},
    {"label": "Qualify for the playoffs (top 8)", "points": 10},
    {"label": "Win Quarterfinal (reach Semifinal)", "points": 15},
    {"label": "Win Semifinal (reach Championship)", "points": 25},
    {"label": "Win the NWSL Championship", "points": 35},
]

# The Tour de France Team Classification is a single once-a-year ranked
# outcome (lowest combined time of each team's best 3 finishers per stage,
# summed across the whole race) rather than a season of games — structurally
# closer to a single golf major than to a league table, so this reuses that
# same placement-tiered shape (GOLF_SCORING_RULES above) rather than
# anything win/loss-based. Tiers are compressed relative to golf's ~150-
# player field to fit a ~23-team classification.
TDF_SCORING_RULES: list[dict] = [
    {"label": "Finishes 16th or worse (of ~23 teams)", "points": 3},
    {"label": "Finishes 11th-15th", "points": 8},
    {"label": "Finishes 6th-10th", "points": 15},
    {"label": "Finishes 4th-5th", "points": 25},
    {"label": "Finishes 3rd", "points": 35},
    {"label": "Finishes 2nd", "points": 45},
    {"label": "Wins the Team Classification", "points": 60},
]

SCORING_RULES: dict[str, list[dict]] = {
    "MLB": [
        {"label": "Regular-season win", "points": 2},
        {"label": "Regular-season loss", "points": -1},
        {"label": "Win division", "points": 5},
        {"label": "Win Division Series (DS)", "points": 15},
        {"label": "Win pennant (LCS)", "points": 30},
        {"label": "Win World Series (WS)", "points": 30},
    ],
    "NFL": [
        {"label": "Regular-season win", "points": 10},
        {"label": "Regular-season tie", "points": 5},
        {"label": "Win Wild Card round (or 1st-round bye)", "points": 10},
        {"label": "Win Divisional round", "points": 20},
        {"label": "Win Conference Championship", "points": 30},
        {"label": "Win Super Bowl", "points": 40},
    ],
    "NBA": [
        {"label": "Regular-season win", "points": 3},
        {"label": "Regular-season loss", "points": -1},
        {"label": "Qualify for playoffs", "points": 10},
        {"label": "Win Round 1", "points": 10},
        {"label": "Win Round 2 (Conf. Semis)", "points": 15},
        {"label": "Win Conference Championship", "points": 25},
        {"label": "Win NBA Championship", "points": 30},
    ],
    "NHL": [
        {"label": "Win (regulation, overtime, or shootout)", "points": 3},
        {"label": "Regulation loss", "points": -1},
        {"label": "Overtime/shootout loss", "points": 2},
        {"label": "Qualify for playoffs", "points": 10},
        {"label": "Win Round 1", "points": 10},
        {"label": "Win Round 2 (Conf. Semis)", "points": 15},
        {"label": "Win Conference Championship", "points": 25},
        {"label": "Win Stanley Cup", "points": 40},
    ],
    "EPL": [
        {"label": "Per point in the league standings", "points": 2},
        {"label": "Per goal of goal differential (GD)", "points": 1},
    ],
    "NCAAF": [
        {"label": "Win (regular season or bowl/playoff game)", "points": 12},
        {"label": "Loss (regular season)", "points": -6},
        {"label": "Loss (bowl or playoff game)", "points": 0},
        {"label": "Playoff bid (make the CFP bracket)", "points": 10},
        {"label": "Playoff win (any round before the title game)", "points": 10},
        {"label": "CFP Championship Game bid", "points": 20},
        {"label": "CFP Championship Game winner", "points": 30},
    ],
    "NCAAMB": CBB_SCORING_RULES,
    "NCAAWB": CBB_SCORING_RULES,
    "ATP": TENNIS_SCORING_RULES,
    "WTA": TENNIS_SCORING_RULES,
    "PGA": GOLF_SCORING_RULES,
    "LPGA": GOLF_SCORING_RULES,
    "F1": F1_SCORING_RULES,
    # Mimics NBA's style (win/loss points + escalating, cumulative playoff-
    # round bonuses) but scaled for a 44-game season (~half of NBA's 82,
    # so win/loss points are doubled: 6/-2 vs NBA's 3/-1, same 3:1 ratio)
    # and a conference-less format — since 2022 the WNBA has used a single
    # unified standings table and an 8-team bracket with no conference
    # stage, so there are 3 playoff rounds here, not NBA's 4.
    "WNBA": [
        {"label": "Regular-season win", "points": 6},
        {"label": "Regular-season loss", "points": -2},
        {"label": "Qualify for playoffs", "points": 10},
        {"label": "Win Round 1", "points": 15},
        {"label": "Win Semifinals", "points": 25},
        {"label": "Win WNBA Championship", "points": 35},
    ],
    # EPL-style base (points + goal differential, identical weights — MLS's
    # 34-game season is close enough to EPL's 38 that no rescaling is
    # needed), plus cumulative playoff-round bonuses in this app's usual
    # style (same magnitudes as NBA/NHL's: 10/10/15/25/30) since MLS,
    # unlike EPL, has a playoff bracket on top of the table. The Supporters'
    # Shield (best overall regular-season record across all 30 teams, no
    # conference split) gets its own bonus, roughly a "division title"
    # tier but scaled up for being a full-league achievement.
    "MLS": [
        {"label": "Per point in the standings", "points": 2},
        {"label": "Per goal of goal differential (GD)", "points": 1},
        {"label": "Win the Supporters' Shield (best overall record)", "points": 15},
        {"label": "Qualify for the playoffs", "points": 10},
        {"label": "Win Round One (reach Conference Semifinals)", "points": 10},
        {"label": "Win Conference Semifinal (reach Conference Final)", "points": 15},
        {"label": "Win Conference Final (reach MLS Cup)", "points": 25},
        {"label": "Win MLS Cup", "points": 30},
    ],
    "NWSL": NWSL_SCORING_RULES,
    "TDF": TDF_SCORING_RULES,
    # EPL-style base (points + a differential term), like MLS — table
    # points already include rugby's own try/losing bonus points, so no
    # separate bonus-point stat is needed. Points difference (PF-PA) swings
    # much wider in rugby than soccer goal differential (a real season can
    # run +/-300), so it's scaled down 10x to land at a similar contribution
    # size to EPL's 1-per-goal GD term. Playoff bonuses use WNBA's 3-round
    # scale (10/15/25/35) since URC's bracket is also exactly 3 rounds
    # (Quarterfinal, Semifinal, Grand Final) — no conference stage.
    "URC": [
        {"label": "Per league table point", "points": 2},
        {"label": "Per 10 points of points difference (PF-PA)", "points": 1},
        {"label": "Qualify for the playoffs (top 8)", "points": 10},
        {"label": "Win Quarterfinal (reach Semifinal)", "points": 15},
        {"label": "Win Semifinal (reach Grand Final)", "points": 25},
        {"label": "Win the Grand Final (champion)", "points": 35},
    ],
    # NFL-style base: real IPL points, like real NFL standings, never
    # penalize a loss (2 pts/win, 1 for a tie/no-result, 0 for a loss), so
    # this mirrors NFL's exact non-punitive shape (10/win, 5/tie, nothing
    # subtracted) rather than the win-minus-loss style most other leagues
    # use — a 14-game IPL season is roughly NFL-scale too. Net Run Rate
    # (the actual real tiebreaker stat, roughly -1.5 to +1.5 in practice)
    # stands in for a differential term, scaled up to land at a similar
    # contribution size to NFL's own implicit win-value scale. IPL's
    # knockout stage is a "page playoff" (Qualifier 1/Eliminator/Qualifier
    # 2/Final), not a clean bracket, so the bonuses track the two
    # meaningful thresholds instead of naming individual rounds: winning
    # any knockout match, and reaching/winning the Final.
    "IPL": [
        {"label": "Regular-season win", "points": 10},
        {"label": "Regular-season tie / no-result", "points": 5},
        {"label": "Per 0.1 of Net Run Rate (NRR)", "points": 2},
        {"label": "Qualify for the playoffs (top 4)", "points": 10},
        {"label": "Win a knockout-stage match (Qualifier/Eliminator)", "points": 15},
        {"label": "Reach the Final", "points": 25},
        {"label": "Win the Final (champion)", "points": 40},
    ],
}


def compute_score(league: str, stats: dict) -> float:
    if league == "MLB":
        return (
            2 * stats["wins"]
            - 1 * stats["losses"]
            + (5 if stats.get("won_division") else 0)
            + (15 if stats.get("won_ds") else 0)
            + (30 if stats.get("won_pennant") else 0)
            + (30 if stats.get("won_ws") else 0)
        )
    if league == "NFL":
        return (
            10 * stats["wins"]
            + 5 * stats.get("ties", 0)
            + (10 if stats.get("won_round1_or_bye") else 0)
            + (20 if stats.get("won_round2") else 0)
            + (30 if stats.get("won_conf_champ") else 0)
            + (40 if stats.get("won_sb") else 0)
        )
    if league == "NBA":
        return (
            3 * stats["wins"]
            - 1 * stats["losses"]
            + (10 if stats.get("made_playoffs") else 0)
            + (10 if stats.get("won_round1") else 0)
            + (15 if stats.get("won_round2") else 0)
            + (25 if stats.get("won_conf_champ") else 0)
            + (30 if stats.get("won_nba_champ") else 0)
        )
    if league == "NHL":
        return (
            3 * stats["wins"]
            - 1 * stats["reg_losses"]
            + 2 * stats["ot_losses"]
            + (10 if stats.get("made_playoffs") else 0)
            + (10 if stats.get("won_round1") else 0)
            + (15 if stats.get("won_round2") else 0)
            + (25 if stats.get("won_conf_champ") else 0)
            + (40 if stats.get("won_cup") else 0)
        )
    if league == "EPL":
        return 2 * stats["standings_points"] + 1 * stats["goal_differential"]
    if league == "NCAAF":
        return (
            12 * stats["wins"]
            - 6 * stats["reg_season_losses"]
            + (10 if stats.get("playoff_bid") else 0)
            + 10 * stats.get("playoff_wins", 0)
            + (20 if stats.get("championship_bid") else 0)
            + (30 if stats.get("championship_win") else 0)
        )
    if league in ("NCAAMB", "NCAAWB"):
        return (
            3 * stats["wins"]
            - 1 * stats["losses"]
            + (5 if stats.get("reg_season_conf_champ") else 0)
            + (10 if stats.get("conf_tourney_champ") else 0)
            + (15 if stats.get("ncaa_qualifier") else 0)
            + (10 if stats.get("seed_1") else 0)
            + (5 if stats.get("seed_2") else 0)
            + (5 if stats.get("won_round_of_64") else 0)
            + (5 if stats.get("won_round_of_32") else 0)
            + (5 if stats.get("won_sweet_16") else 0)
            + (10 if stats.get("won_elite_8") else 0)
            + (10 if stats.get("won_final_4") else 0)
            + (25 if stats.get("won_championship") else 0)
        )
    if league in ("ATP", "WTA"):
        # stats counts how many of the country's players won each round —
        # not booleans, since a country can have multiple entrants at a
        # major. Round wins stack cumulatively per player (see wiki).
        return (
            2 * stats.get("round_1_wins", 0)
            + 3 * stats.get("round_2_wins", 0)
            + 5 * stats.get("round_3_wins", 0)
            + 5 * stats.get("round_4_wins", 0)
            + 7 * stats.get("quarterfinal_wins", 0)
            + 8 * stats.get("semifinal_wins", 0)
            + 10 * stats.get("final_wins", 0)
        )
    if league in ("PGA", "LPGA"):
        # stats counts how many of the letter's players achieved each
        # result at the major — not booleans, since a letter can have
        # multiple players in the field. Placement bands are NOT cumulative
        # with each other (a player finishes in exactly one place); the
        # made-cut count stacks additively on top of whichever band applies.
        return (
            10 * stats.get("made_cut_count", 0)
            + 5 * stats.get("place_21_30_count", 0)
            + 7 * stats.get("place_16_20_count", 0)
            + 9 * stats.get("place_11_15_count", 0)
            + 10 * stats.get("place_10_count", 0)
            + 11 * stats.get("place_9_count", 0)
            + 12 * stats.get("place_8_count", 0)
            + 14 * stats.get("place_7_count", 0)
            + 16 * stats.get("place_6_count", 0)
            + 18 * stats.get("place_5_count", 0)
            + 20 * stats.get("place_4_count", 0)
            + 25 * stats.get("place_3_count", 0)
            + 35 * stats.get("place_2_count", 0)
            + 50 * stats.get("place_1_count", 0)
        )
    if league == "F1":
        return (
            1 * stats.get("points_finishes", 0)
            - 1 * stats.get("non_points_finishes", 0)
            + 3 * stats.get("podiums", 0)
            + 5 * stats.get("wins", 0)
            + 2 * stats.get("poles", 0)
            + 1 * stats.get("fastest_laps", 0)
            + 1 * stats.get("sprint_points_finishes", 0)
            + 1 * stats.get("sprint_podiums", 0)
            + 2 * stats.get("sprint_wins", 0)
            + (30 if stats.get("championship_place") == 1 else 0)
            + (18 if stats.get("championship_place") == 2 else 0)
            + (10 if stats.get("championship_place") == 3 else 0)
        )
    if league == "WNBA":
        return (
            6 * stats["wins"]
            - 2 * stats["losses"]
            + (10 if stats.get("made_playoffs") else 0)
            + (15 if stats.get("won_round1") else 0)
            + (25 if stats.get("won_semis") else 0)
            + (35 if stats.get("won_wnba_champ") else 0)
        )
    if league == "MLS":
        return (
            2 * stats["standings_points"]
            + 1 * stats["goal_differential"]
            + (15 if stats.get("won_shield") else 0)
            + (10 if stats.get("made_playoffs") else 0)
            + (10 if stats.get("won_round1") else 0)
            + (15 if stats.get("won_conf_semi") else 0)
            + (25 if stats.get("won_conf_final") else 0)
            + (30 if stats.get("won_mls_cup") else 0)
        )
    if league == "NWSL":
        return (
            2 * stats["standings_points"]
            + stats["goal_differential"]
            + (15 if stats.get("won_shield") else 0)
            + (10 if stats.get("made_playoffs") else 0)
            + (15 if stats.get("won_quarterfinal") else 0)
            + (25 if stats.get("won_semifinal") else 0)
            + (35 if stats.get("won_championship") else 0)
        )
    if league == "TDF":
        place = stats["place"]
        if place == 1:
            return 60
        if place == 2:
            return 45
        if place == 3:
            return 35
        if place <= 5:
            return 25
        if place <= 10:
            return 15
        if place <= 15:
            return 8
        return 3
    if league == "URC":
        return round(
            2 * stats["table_points"]
            + 0.1 * stats["points_difference"]
            + (10 if stats.get("made_playoffs") else 0)
            + (15 if stats.get("won_quarterfinal") else 0)
            + (25 if stats.get("won_semifinal") else 0)
            + (35 if stats.get("won_final") else 0)
        )
    if league == "IPL":
        return round(
            10 * stats["wins"]
            + 5 * stats.get("ties", 0)
            + 20 * stats.get("net_run_rate", 0)
            + (10 if stats.get("made_playoffs") else 0)
            + 15 * stats.get("knockout_wins", 0)
            + (25 if stats.get("reached_final") else 0)
            + (40 if stats.get("won_final") else 0)
        )

    raise ValueError(f"Unknown league: {league}")
