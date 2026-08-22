"""Reference content for the Team History page: a short biography plus
enough real historical season stats to chart "fantasy points" (via
league_rules.compute_score) across the last several seasons a team
actually played in its league.

Deliberately structured like set_ev_defaults.py's FALL_EV_RAW_SCORES --
plain content-as-code, no migration needed. This is a test of the feature
scoped to EPL only; extend TEAM_BIOS/TEAM_HISTORY_STATS/TEAM_LOCATIONS
with the same shape to cover another league.

TEAM_HISTORY_STATS intentionally stops one season short of "now" -- the
most recent season lives in the Team_season_results table already (the
same row Example Scores reads), so the history endpoint reads that live
rather than duplicating it here and letting it drift stale once someone
updates that row for a new season.
"""

# (league, team name) -> (latitude, longitude) of the team's home ground,
# for the "where they play" map. Approximate stadium coordinates.
TEAM_LOCATIONS: dict[tuple[str, str], tuple[float, float]] = {
    ("EPL", "Arsenal"): (51.5549, -0.1084),  # Emirates Stadium, London
    ("EPL", "Aston Villa"): (52.5092, -1.8848),  # Villa Park, Birmingham
    ("EPL", "Bournemouth"): (50.7352, -1.8384),  # Vitality Stadium
    ("EPL", "Brentford"): (51.4907, -0.2886),  # Gtech Community Stadium, London
    ("EPL", "Brighton & Hove Albion"): (50.8617, -0.0837),  # Amex Stadium, Falmer
    ("EPL", "Chelsea"): (51.4816, -0.1910),  # Stamford Bridge, London
    ("EPL", "Coventry City"): (52.4483, -1.4954),  # CBS Arena, Coventry
    ("EPL", "Crystal Palace"): (51.3983, -0.0856),  # Selhurst Park, London
    ("EPL", "Everton"): (53.4483, -2.9925),  # Everton Stadium, Bramley-Moore Dock
    ("EPL", "Fulham"): (51.4749, -0.2217),  # Craven Cottage, London
    ("EPL", "Hull City"): (53.7460, -0.3672),  # MKM Stadium
    ("EPL", "Ipswich Town"): (52.0552, 1.1451),  # Portman Road
    ("EPL", "Leeds United"): (53.7778, -1.5722),  # Elland Road
    ("EPL", "Liverpool"): (53.4308, -2.9608),  # Anfield
    ("EPL", "Manchester City"): (53.4831, -2.2004),  # Etihad Stadium
    ("EPL", "Manchester United"): (53.4631, -2.2913),  # Old Trafford
    ("EPL", "Newcastle United"): (54.9756, -1.6217),  # St James' Park
    ("EPL", "Nottingham Forest"): (52.9400, -1.1328),  # City Ground
    ("EPL", "Sunderland"): (54.9144, -1.3883),  # Stadium of Light
    ("EPL", "Tottenham Hotspur"): (51.6043, -0.0662),  # Tottenham Hotspur Stadium, London
}

# (league, team name) -> a short factual biography (2-4 sentences):
# founding, home ground, identity/nickname, and a headline moment or two.
TEAM_BIOS: dict[tuple[str, str], str] = {
    ("EPL", "Arsenal"): (
        "Founded in 1886 and based in north London at the Emirates Stadium since 2006 "
        "(previously Highbury), Arsenal are nicknamed the Gunners and hold the record for "
        "most FA Cups won (14). Their 2003-04 \"Invincibles\" remain the only side to go a "
        "full 38-game Premier League season unbeaten."
    ),
    ("EPL", "Aston Villa"): (
        "Founded in 1874 and playing at Villa Park in Birmingham, Aston Villa were a "
        "founding member of both the Football League (1888) and the Premier League (1992). "
        "They remain the last English club outside the traditional \"big clubs\" to win the "
        "European Cup, in 1982."
    ),
    ("EPL", "Bournemouth"): (
        "Founded in 1899 and based at the Vitality Stadium on the English south coast, "
        "Bournemouth reached the Premier League for the first time in their history in 2015 "
        "under manager Eddie Howe, a rapid rise from League Two a decade earlier."
    ),
    ("EPL", "Brentford"): (
        "Founded in 1889 in west London and now playing at the Gtech Community Stadium "
        "(previously Griffin Park), Brentford returned to the top flight in 2021 after a "
        "74-year absence, built on data-driven recruitment under co-owner Matthew Benham."
    ),
    ("EPL", "Brighton & Hove Albion"): (
        "Founded in 1901 and based at the Falmer/American Express Stadium since 2011, "
        "Brighton reached the Premier League in 2017 for the first time since 1983. The "
        "Seagulls have since built a reputation for shrewd recruitment and developing "
        "players who move on to bigger clubs."
    ),
    ("EPL", "Chelsea"): (
        "Founded in 1905 and based at Stamford Bridge in west London, Chelsea have won six "
        "English league titles and two Champions Leagues (2012, 2021). Heavy investment "
        "under owner Roman Abramovich (2003-2022) transformed the club into a regular "
        "trophy contender; a Clearlake/Boehly-led consortium has owned it since 2022."
    ),
    ("EPL", "Coventry City"): (
        "Founded in 1883 and nicknamed the Sky Blues, Coventry's only major honour is the "
        "1987 FA Cup. They spent 34 straight seasons in the top flight from 1967 to 2001 "
        "before relegation; 2026-27 marks their first return to the Premier League since."
    ),
    ("EPL", "Crystal Palace"): (
        "Founded in 1905 and based at Selhurst Park in south London, the Eagles have been "
        "a fixture of the Premier League since promotion in 2013. They won their first "
        "major trophy, the FA Cup, in 2025, beating Manchester City in the final."
    ),
    ("EPL", "Everton"): (
        "Founded in 1878, Everton played at Goodison Park from 1892 before moving to "
        "Everton Stadium at Bramley-Moore Dock in 2025. Nicknamed the Toffees, they held "
        "one of English football's longest unbroken top-flight streaks before eventually "
        "being relegated from it."
    ),
    ("EPL", "Fulham"): (
        "Founded in 1879 and based at Craven Cottage on the Thames in west London, Fulham "
        "are London's oldest professional football club. Nicknamed the Cottagers, they "
        "reached the UEFA Europa League final in 2010 under Roy Hodgson."
    ),
    ("EPL", "Hull City"): (
        "Founded in 1904 and nicknamed the Tigers, Hull City first reached the Premier "
        "League in 2008-09 and reached the FA Cup final in 2014. They last played "
        "top-flight football in 2016-17; 2026-27 marks their return after nearly a decade."
    ),
    ("EPL", "Ipswich Town"): (
        "Founded in 1878 and based at Portman Road, Ipswich won the English league title "
        "in 1961-62 and the UEFA Cup in 1981 under Bobby Robson. After 22 years away, they "
        "were promoted to the Premier League in 2024, relegated after one season back, and "
        "return again for 2026-27."
    ),
    ("EPL", "Leeds United"): (
        "Founded in 1919 and based at Elland Road, Leeds won the old First Division three "
        "times (1969, 1974, 1992) and reached a Champions League semifinal in 2001. A "
        "financial collapse sent them out of the top flight for 16 years (2004-2020); "
        "they've moved between the Premier League and Championship since."
    ),
    ("EPL", "Liverpool"): (
        "Founded in 1892 and based at Anfield, Liverpool are one of England's most "
        "decorated clubs with 19 league titles and six European Cups. Arne Slot has "
        "managed the side since 2024, succeeding the hugely successful Jurgen Klopp era."
    ),
    ("EPL", "Manchester City"): (
        "Founded in 1880 and based at the Etihad Stadium in east Manchester, City became "
        "the dominant force in English football through the 2010s and 2020s under owner "
        "Sheikh Mansour (since 2008) and manager Pep Guardiola (since 2016), completing a "
        "domestic and European treble in 2022-23."
    ),
    ("EPL", "Manchester United"): (
        "Founded in 1878 as Newton Heath and based at Old Trafford, United hold the "
        "record for most English league titles (20). Sir Alex Ferguson's 1986-2013 "
        "tenure, capped by the 1999 treble, is the most successful era in the club's "
        "history; results have been far less consistent since."
    ),
    ("EPL", "Newcastle United"): (
        "Founded in 1892 and based at St James' Park, Newcastle have one of English "
        "football's most passionate fanbases. A Saudi Arabia-backed takeover in 2021 "
        "brought heavy investment, and the Magpies won the League Cup in 2025, their "
        "first major trophy since 1969."
    ),
    ("EPL", "Nottingham Forest"): (
        "Founded in 1865 and based at the City Ground, Forest won back-to-back European "
        "Cups in 1979 and 1980 under Brian Clough, a remarkable feat for a club of their "
        "size. Promoted back to the Premier League in 2022 after 23 years away, they "
        "finished 7th and qualified for Europe in 2024-25."
    ),
    ("EPL", "Sunderland"): (
        "Founded in 1879 and based at the Stadium of Light, Sunderland are six-time "
        "English champions, almost all before the Second World War. After relegation as "
        "far as League One in 2018, the Black Cats worked back up and returned to the "
        "Premier League via the 2025 Championship play-offs."
    ),
    ("EPL", "Tottenham Hotspur"): (
        "Founded in 1882 and based at the Tottenham Hotspur Stadium (opened 2019, "
        "previously White Hart Lane), Spurs were the first English club to win a European "
        "trophy (the 1963 Cup Winners' Cup) and the first to complete the modern domestic "
        "double (1961). They won the UEFA Europa League in 2025, ending a 17-year wait "
        "for a trophy."
    ),
}

# (league, team name) -> {season_label: stats}, same stats shape
# league_rules.compute_score expects for that league (for EPL:
# standings_points, goal_differential). Only seasons the team actually
# played in this league are listed -- a promoted/relegated club's history
# has real gaps, which is correct, not a data error. Sourced from each
# season's final Premier League table.
TEAM_HISTORY_STATS: dict[tuple[str, str], dict[str, dict]] = {
    ("EPL", "Arsenal"): {
        "2021-22": {"standings_points": 69, "goal_differential": 13},
        "2022-23": {"standings_points": 84, "goal_differential": 45},
        "2023-24": {"standings_points": 89, "goal_differential": 62},
        "2024-25": {"standings_points": 74, "goal_differential": 35},
    },
    ("EPL", "Aston Villa"): {
        "2021-22": {"standings_points": 45, "goal_differential": -2},
        "2022-23": {"standings_points": 61, "goal_differential": 5},
        "2023-24": {"standings_points": 68, "goal_differential": 15},
        "2024-25": {"standings_points": 66, "goal_differential": 7},
    },
    ("EPL", "Bournemouth"): {
        # Relegated after 2019-20; not in the Premier League in 2021-22.
        "2022-23": {"standings_points": 39, "goal_differential": -34},
        "2023-24": {"standings_points": 48, "goal_differential": -13},
        "2024-25": {"standings_points": 56, "goal_differential": 12},
    },
    ("EPL", "Brentford"): {
        "2021-22": {"standings_points": 46, "goal_differential": -8},
        "2022-23": {"standings_points": 59, "goal_differential": 12},
        "2023-24": {"standings_points": 39, "goal_differential": -9},
        "2024-25": {"standings_points": 56, "goal_differential": 9},
    },
    ("EPL", "Brighton & Hove Albion"): {
        "2021-22": {"standings_points": 51, "goal_differential": -2},
        "2022-23": {"standings_points": 62, "goal_differential": 19},
        "2023-24": {"standings_points": 48, "goal_differential": -7},
        "2024-25": {"standings_points": 61, "goal_differential": 7},
    },
    ("EPL", "Chelsea"): {
        "2021-22": {"standings_points": 74, "goal_differential": 43},
        "2022-23": {"standings_points": 44, "goal_differential": -9},
        "2023-24": {"standings_points": 63, "goal_differential": 14},
        "2024-25": {"standings_points": 69, "goal_differential": 21},
    },
    # Coventry City: last played in the top flight in 2000-01, well
    # outside the range of comparable data covered so far -- no recent
    # seasons to chart yet.
    ("EPL", "Crystal Palace"): {
        "2021-22": {"standings_points": 48, "goal_differential": 4},
        "2022-23": {"standings_points": 45, "goal_differential": -9},
        "2023-24": {"standings_points": 49, "goal_differential": -1},
        "2024-25": {"standings_points": 53, "goal_differential": 0},
    },
    ("EPL", "Everton"): {
        "2021-22": {"standings_points": 39, "goal_differential": -23},
        "2022-23": {"standings_points": 36, "goal_differential": -23},
        "2023-24": {"standings_points": 40, "goal_differential": -11},
        "2024-25": {"standings_points": 48, "goal_differential": -2},
    },
    ("EPL", "Fulham"): {
        # Relegated after 2020-21; not in the Premier League in 2021-22.
        "2022-23": {"standings_points": 52, "goal_differential": 2},
        "2023-24": {"standings_points": 47, "goal_differential": -6},
        "2024-25": {"standings_points": 54, "goal_differential": 0},
    },
    # Hull City: last played in the top flight in 2016-17 -- no recent
    # seasons to chart yet.
    ("EPL", "Ipswich Town"): {
        "2024-25": {"standings_points": 22, "goal_differential": -46},
    },
    ("EPL", "Leeds United"): {
        "2021-22": {"standings_points": 38, "goal_differential": -37},
        "2022-23": {"standings_points": 31, "goal_differential": -30},
        # Relegated after 2022-23; spent 2023-24 and 2024-25 in the
        # Championship before promotion back for 2025-26.
    },
    ("EPL", "Liverpool"): {
        "2021-22": {"standings_points": 92, "goal_differential": 68},
        "2022-23": {"standings_points": 67, "goal_differential": 28},
        "2023-24": {"standings_points": 82, "goal_differential": 45},
        "2024-25": {"standings_points": 84, "goal_differential": 45},
    },
    ("EPL", "Manchester City"): {
        "2021-22": {"standings_points": 93, "goal_differential": 73},
        "2022-23": {"standings_points": 89, "goal_differential": 61},
        "2023-24": {"standings_points": 91, "goal_differential": 62},
        "2024-25": {"standings_points": 71, "goal_differential": 28},
    },
    ("EPL", "Manchester United"): {
        "2021-22": {"standings_points": 58, "goal_differential": 0},
        "2022-23": {"standings_points": 75, "goal_differential": 15},
        "2023-24": {"standings_points": 60, "goal_differential": -1},
        "2024-25": {"standings_points": 42, "goal_differential": -10},
    },
    ("EPL", "Newcastle United"): {
        "2021-22": {"standings_points": 49, "goal_differential": -18},
        "2022-23": {"standings_points": 71, "goal_differential": 35},
        "2023-24": {"standings_points": 60, "goal_differential": 23},
        "2024-25": {"standings_points": 66, "goal_differential": 21},
    },
    ("EPL", "Nottingham Forest"): {
        # Promoted for 2022-23; not in the Premier League in 2021-22.
        "2022-23": {"standings_points": 38, "goal_differential": -30},
        "2023-24": {"standings_points": 32, "goal_differential": -18},
        "2024-25": {"standings_points": 65, "goal_differential": 12},
    },
    # Sunderland: promoted for 2025-26 after last playing top-flight
    # football in 2016-17 -- no other recent seasons to chart yet.
    ("EPL", "Tottenham Hotspur"): {
        "2021-22": {"standings_points": 71, "goal_differential": 29},
        "2022-23": {"standings_points": 60, "goal_differential": 7},
        "2023-24": {"standings_points": 66, "goal_differential": 13},
        "2024-25": {"standings_points": 38, "goal_differential": -1},
    },
}
