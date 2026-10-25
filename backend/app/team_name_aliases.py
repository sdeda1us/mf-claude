"""Known (league, external_name) -> canonical seed.py Team.name aliases.

External sources (ESPN, web search results, etc.) don't always spell a
team the same way seed.py does -- e.g. ESPN's NBA scoreboard says "LA
Clippers" where seed.py's NBA_TEAMS has "Los Angeles Clippers". Without
normalizing, daily_games_sync/daily_results_sync's exact-match lookup
against Team.name silently misses, leaving the game unowned (games-sync)
or unmatched/skipped (results-sync) even though the team is rostered.

Entries below were found by diffing one-off ESPN API pulls (scoreboards
and, later, standings) against seed.py's team lists -- add to this table
as new mismatches turn up from whatever source feeds the various
daily/espn_*_sync modules, not just ESPN specifically. A league's
scoreboard and standings endpoints don't always spell a team the same
way (e.g. UCL's scoreboard says "Roma", standings says "AS Roma") -- both
spellings need their own entry here, there's no single ESPN-side source
of truth to normalize against once instead.
"""

TEAM_NAME_ALIASES: dict[tuple[str, str], str] = {
    ("NBA", "LA Clippers"): "Los Angeles Clippers",
    ("EPL", "AFC Bournemouth"): "Bournemouth",
    ("URC", "Benetton Treviso"): "Benetton",
    ("URC", "Cardiff Blues"): "Cardiff",
    ("URC", "Zebre"): "Zebre Parma",
    ("UCL", "Viking FK"): "Viking",
    ("UCL", "Internazionale"): "Inter Milan",
    ("UCL", "LASK Linz"): "LASK",
    ("UCL", "Feyenoord Rotterdam"): "Feyenoord",
    ("UCL", "AS Roma"): "Roma",
    ("UCL", "FC Porto"): "Porto",
    ("UCL", "Fenerbahce"): "Fenerbahçe",
    ("UCL", "PSV Eindhoven"): "PSV",
    ("UCL", "Bodo/Glimt"): "Bodø/Glimt",
    ("NCAAF", "Miami Hurricanes"): "Miami (FL) Hurricanes",
    ("NCAAF", "Hawai'i Rainbow Warriors"): "Hawaii Rainbow Warriors",
    ("NCAAF", "San José State Spartans"): "San Jose State Spartans",
    ("NCAAF", "UL Monroe Warhawks"): "Louisiana-Monroe Warhawks",
    ("NCAAF", "App State Mountaineers"): "Appalachian State Mountaineers",
    ("NCAAF", "Florida International Panthers"): "FIU Panthers",
    ("NCAAF", "Massachusetts Minutemen"): "UMass Minutemen",
}


def canonicalize_team_name(league: str, name: str) -> str:
    """Returns the seed.py-canonical name for (league, name) if a known
    alias exists, otherwise returns name unchanged."""
    return TEAM_NAME_ALIASES.get((league, name), name)
