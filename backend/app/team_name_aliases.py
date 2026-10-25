"""Known (league, external_name) -> canonical seed.py Team.name aliases.

External sources (ESPN, web search results, etc.) don't always spell a
team the same way seed.py does -- e.g. ESPN's NBA scoreboard says "LA
Clippers" where seed.py's NBA_TEAMS has "Los Angeles Clippers". Without
normalizing, daily_games_sync/daily_results_sync's exact-match lookup
against Team.name silently misses, leaving the game unowned (games-sync)
or unmatched/skipped (results-sync) even though the team is rostered.

Entries below were found by diffing a one-off ESPN API pull against
seed.py's team lists for the 7 TODAYS_GAMES_LEAGUES (see espn_test/) --
add to this table as new mismatches turn up from whatever source feeds
daily_games_sync/daily_results_sync, not just ESPN specifically.
"""

TEAM_NAME_ALIASES: dict[tuple[str, str], str] = {
    ("NBA", "LA Clippers"): "Los Angeles Clippers",
    ("EPL", "AFC Bournemouth"): "Bournemouth",
    ("URC", "Benetton Treviso"): "Benetton",
    ("UCL", "Viking FK"): "Viking",
    ("UCL", "Internazionale"): "Inter Milan",
    ("UCL", "LASK Linz"): "LASK",
    ("UCL", "Feyenoord Rotterdam"): "Feyenoord",
    ("NCAAF", "Miami Hurricanes"): "Miami (FL) Hurricanes",
    ("NCAAF", "Hawai'i Rainbow Warriors"): "Hawaii Rainbow Warriors",
    ("NCAAF", "San José State Spartans"): "San Jose State Spartans",
    ("NCAAF", "UL Monroe Warhawks"): "Louisiana-Monroe Warhawks",
}


def canonicalize_team_name(league: str, name: str) -> str:
    """Returns the seed.py-canonical name for (league, name) if a known
    alias exists, otherwise returns name unchanged."""
    return TEAM_NAME_ALIASES.get((league, name), name)
