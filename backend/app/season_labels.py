"""The current real-world season_label for each league the daily score
sync covers (app/daily_score_sync.py) -- separate from league_rules.py,
which is specifically scoring formulas per its own docstring.

Convention (established by seed_historical_results.py's LEAGUE_SEASONS):
single-calendar-year labels like "2026" for leagues whose season doesn't
cross a new year (NFL, NCAAF, ATP, WTA among the leagues covered here),
cross-year labels like "2026-27" for leagues whose season does (NBA, NHL,
EPL, UCL, URC among the leagues covered here).

Update this dict once a year as each league's season rolls over -- see
CLAUDE.md's "Sports Leagues" section for real-world season windows.
"""

CURRENT_SEASON: dict[str, str] = {
    "NFL": "2026",
    "NCAAF": "2026",
    "ATP": "2026",
    "WTA": "2026",
    "NBA": "2026-27",
    "NHL": "2026-27",
    "EPL": "2026-27",
    "UCL": "2026-27",
    "URC": "2026-27",
}
