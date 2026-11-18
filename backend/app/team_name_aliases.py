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
    ("NCAAMB", "UAlbany Great Danes"): "Albany Great Danes",
    ("NCAAMB", "American University Eagles"): "American Eagles",
    ("NCAAMB", "App State Mountaineers"): "Appalachian State Mountaineers",
    ("NCAAMB", "Florida International Panthers"): "FIU Panthers",
    ("NCAAMB", "Grambling Tigers"): "Grambling State Tigers",
    ("NCAAMB", "Grand Canyon Lopes"): "Grand Canyon Antelopes",
    ("NCAAMB", "Hawai'i Rainbow Warriors"): "Hawaii Rainbow Warriors",
    ("NCAAMB", "IU Indianapolis Jaguars"): "IU Indy Jaguars",
    ("NCAAMB", "Long Island University Sharks"): "LIU Sharks",
    ("NCAAMB", "UL Monroe Warhawks"): "Louisiana-Monroe Warhawks",
    ("NCAAMB", "McNeese Cowboys"): "McNeese State Cowboys",
    ("NCAAMB", "Miami Hurricanes"): "Miami (FL) Hurricanes",
    ("NCAAMB", "North Carolina A&T Aggies"): "NC A&T Aggies",
    ("NCAAMB", "LSU New Orleans Privateers"): "New Orleans Privateers",
    ("NCAAMB", "Nicholls Colonels"): "Nicholls State Colonels",
    ("NCAAMB", "Pennsylvania Quakers"): "Penn Quakers",
    ("NCAAMB", "Queens University Royals"): "Queens Royals",
    ("NCAAMB", "San José State Spartans"): "San Jose State Spartans",
    ("NCAAMB", "Seattle U Redhawks"): "Seattle Redhawks",
    ("NCAAMB", "SE Louisiana Lions"): "Southeastern Louisiana Lions",
    ("NCAAMB", "Massachusetts Minutemen"): "UMass Minutemen",
    ("NCAAMB", "South Carolina Upstate Spartans"): "USC Upstate Spartans",
    ("NCAAWB", "Alabama State Lady Hornets"): "Alabama State Hornets",
    ("NCAAWB", "UAlbany Great Danes"): "Albany Great Danes",
    ("NCAAWB", "Alcorn State Lady Braves"): "Alcorn State Braves",
    ("NCAAWB", "American University Eagles"): "American Eagles",
    ("NCAAWB", "App State Mountaineers"): "Appalachian State Mountaineers",
    ("NCAAWB", "Central Arkansas Sugar Bears"): "Central Arkansas Bears",
    ("NCAAWB", "Florida International Panthers"): "FIU Panthers",
    ("NCAAWB", "Georgia Lady Bulldogs"): "Georgia Bulldogs",
    ("NCAAWB", "Grambling Lady Tigers"): "Grambling State Tigers",
    ("NCAAWB", "Grand Canyon Lopes"): "Grand Canyon Antelopes",
    ("NCAAWB", "Hampton Lady Pirates"): "Hampton Pirates",
    ("NCAAWB", "Hawai'i Rainbow Wahine"): "Hawaii Rainbow Warriors",
    ("NCAAWB", "IU Indianapolis Jaguars"): "IU Indy Jaguars",
    ("NCAAWB", "Jackson State Lady Tigers"): "Jackson State Tigers",
    ("NCAAWB", "Long Island University Sharks"): "LIU Sharks",
    ("NCAAWB", "Louisiana Tech Lady Techsters"): "Louisiana Tech Bulldogs",
    ("NCAAWB", "UL Monroe Warhawks"): "Louisiana-Monroe Warhawks",
    ("NCAAWB", "McNeese Cowgirls"): "McNeese State Cowboys",
    ("NCAAWB", "Miami Hurricanes"): "Miami (FL) Hurricanes",
    ("NCAAWB", "Mississippi Valley State Devilettes"): "Mississippi Valley State Delta Devils",
    ("NCAAWB", "Missouri State Lady Bears"): "Missouri State Bears",
    ("NCAAWB", "Montana Lady Griz"): "Montana Grizzlies",
    ("NCAAWB", "Morgan State Lady Bears"): "Morgan State Bears",
    ("NCAAWB", "North Carolina A&T Aggies"): "NC A&T Aggies",
    ("NCAAWB", "LSU New Orleans Privateers"): "New Orleans Privateers",
    ("NCAAWB", "Nicholls Colonels"): "Nicholls State Colonels",
    ("NCAAWB", "Northwestern State Lady Demons"): "Northwestern State Demons",
    ("NCAAWB", "Oklahoma State Cowgirls"): "Oklahoma State Cowboys",
    ("NCAAWB", "Pennsylvania Quakers"): "Penn Quakers",
    ("NCAAWB", "Penn State Lady Lions"): "Penn State Nittany Lions",
    ("NCAAWB", "Prairie View A&M Lady Panthers"): "Prairie View A&M Panthers",
    ("NCAAWB", "Queens University Royals"): "Queens Royals",
    ("NCAAWB", "San José State Spartans"): "San Jose State Spartans",
    ("NCAAWB", "Seattle U Redhawks"): "Seattle Redhawks",
    ("NCAAWB", "South Carolina State Lady Bulldogs"): "South Carolina State Bulldogs",
    ("NCAAWB", "SE Louisiana Lady Lions"): "Southeastern Louisiana Lions",
    ("NCAAWB", "Southern Miss Lady Eagles"): "Southern Miss Golden Eagles",
    ("NCAAWB", "Stephen F. Austin Ladyjacks"): "Stephen F. Austin Lumberjacks",
    ("NCAAWB", "Tennessee Lady Volunteers"): "Tennessee Volunteers",
    ("NCAAWB", "Tennessee State Lady Tigers"): "Tennessee State Tigers",
    ("NCAAWB", "Texas Tech Lady Raiders"): "Texas Tech Red Raiders",
    ("NCAAWB", "Massachusetts Minutewomen"): "UMass Minutemen",
    ("NCAAWB", "UNLV Lady Rebels"): "UNLV Rebels",
    ("NCAAWB", "South Carolina Upstate Spartans"): "USC Upstate Spartans",
    ("NCAAWB", "Western Kentucky Lady Toppers"): "Western Kentucky Hilltoppers",
    ("NCAAWB", "Wyoming Cowgirls"): "Wyoming Cowboys",
}


def canonicalize_team_name(league: str, name: str) -> str:
    """Returns the seed.py-canonical name for (league, name) if a known
    alias exists, otherwise returns name unchanged."""
    return TEAM_NAME_ALIASES.get((league, name), name)
