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

from sqlalchemy.orm import Session

from app.models import Team, TeamSeasonResult

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

# All-zero stats, shaped exactly as league_rules.compute_score expects for
# that league -- used only to seed a placeholder TeamSeasonResult the
# moment a team is newly rostered, in a league/season the daily sync
# hasn't produced real data for yet (NBA pre-tipoff, ATP/WTA outside a
# major window, or just before that league's first sync of the cycle).
# Without this, scoring_summary's "most recent TeamSeasonResult" lookup
# falls back to that team's last REAL season's row (if one exists) --
# reading as a nonzero head start instead of the 0 it should be, exactly
# the gap update_live_standings.py's old hardcoded team lists left for
# any rostered team they didn't happen to cover.
ZERO_STATS: dict[str, dict] = {
    "NFL": {
        "wins": 0,
        "ties": 0,
        "won_round1_or_bye": False,
        "won_round2": False,
        "won_conf_champ": False,
        "won_sb": False,
    },
    "NCAAF": {
        "wins": 0,
        "reg_season_losses": 0,
        "playoff_bid": False,
        "playoff_wins": 0,
        "playoff_bye": False,
        "championship_bid": False,
        "championship_win": False,
    },
    "ATP": {
        "round_1_wins": 0,
        "round_2_wins": 0,
        "round_3_wins": 0,
        "round_4_wins": 0,
        "quarterfinal_wins": 0,
        "semifinal_wins": 0,
        "final_wins": 0,
    },
    "WTA": {
        "round_1_wins": 0,
        "round_2_wins": 0,
        "round_3_wins": 0,
        "round_4_wins": 0,
        "quarterfinal_wins": 0,
        "semifinal_wins": 0,
        "final_wins": 0,
    },
    "NBA": {
        "wins": 0,
        "losses": 0,
        "made_playoffs": False,
        "won_round1": False,
        "won_round2": False,
        "won_conf_champ": False,
        "won_nba_champ": False,
    },
    "NHL": {
        "reg_wins": 0,
        "reg_losses": 0,
        "ot_so_wins": 0,
        "ot_so_losses": 0,
        "made_playoffs": False,
        "won_round1": False,
        "won_round2": False,
        "won_conf_champ": False,
        "won_cup": False,
    },
    "EPL": {"standings_points": 0, "goal_differential": 0},
    "UCL": {
        "points": 0,
        "goal_differential": 0,
        "made_final_24": False,
        "made_final_16": False,
        "made_final_8": False,
        "made_final_4": False,
        "made_final_2": False,
        "won_final": False,
    },
    "URC": {
        "table_points": 0,
        "points_difference": 0,
        "made_playoffs": False,
        "won_quarterfinal": False,
        "won_semifinal": False,
        "won_final": False,
    },
}


def ensure_current_season_placeholder(db: Session, team: Team) -> None:
    """Call whenever a team is newly rostered. Creates an all-zero
    TeamSeasonResult for the current real-world season if this team
    doesn't have one yet -- never overwrites a row the daily sync (or
    anything else) already wrote. No-op for a league outside the daily
    sync's scope (CURRENT_SEASON), since nothing here ever resolves
    "most recent" for those anyway."""
    season_label = CURRENT_SEASON.get(team.league)
    if season_label is None:
        return
    existing = (
        db.query(TeamSeasonResult)
        .filter(TeamSeasonResult.team_id == team.id, TeamSeasonResult.season_label == season_label)
        .first()
    )
    if existing is not None:
        return
    db.add(
        TeamSeasonResult(
            team_id=team.id,
            league=team.league,
            season_label=season_label,
            stats=ZERO_STATS.get(team.league, {}),
        )
    )
