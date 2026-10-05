"""Turns two consecutive days' TeamDailyScore stats into a list of
human-readable, point-valued events -- "what changed, and how many points
was it worth" -- for the Seasons page's "Recent Activity" feed
(routers/seasons.py's league_events endpoint).

COUNT_EVENTS/FLAG_EVENTS below mirror league_rules.compute_score's
coefficients for the 9 daily-synced leagues (NFL, NBA, NHL, EPL, NCAAF,
ATP, WTA, UCL, URC) -- confirmed by re-reading compute_score directly that
every one of these 9 is a simple linear combination of stat keys (a count
times a point value, or a flat bonus for a boolean flag), unlike golf's
placement bands or PGA/LPGA's letter aggregation (neither of which is in
the daily sync's scope). Deliberately a SEPARATE table from compute_score
rather than a refactor of it -- mild duplication, but zero risk of
regressing the scoring engine itself. Keep both in sync when a league's
scoring rules change (see migrate_nhl_win_split.py for a recent example of
what a key-shape change here looks like).

EPL/UCL/URC only ever report composite deltas ("standings points +3", "GD
+2") rather than "won/drew/lost a game" -- the daily sync's source data for
these leagues is a cumulative points+GD pair, not discrete win/draw/loss
counts, so there's nothing more specific available to report.
"""

# league -> {stat key: (label, points per unit)} for anything that accumulates.
COUNT_EVENTS: dict[str, dict[str, tuple[str, float]]] = {
    "NFL": {
        "wins": ("won a game", 10),
        "ties": ("tied a game", 5),
    },
    "NBA": {
        "wins": ("won a game", 3),
        "losses": ("lost a game", -1),
    },
    "NHL": {
        "reg_wins": ("won in regulation", 3),
        "reg_losses": ("lost in regulation", -1),
        "ot_so_wins": ("won in OT/shootout", 2),
        "ot_so_losses": ("lost in OT/shootout", 0),
    },
    "EPL": {
        "standings_points": ("earned standings points", 2),
        "goal_differential": ("goal differential moved", 1),
    },
    "NCAAF": {
        "wins": ("won a game", 12),
        "reg_season_losses": ("lost a regular-season game", -6),
        "playoff_wins": ("won a playoff round", 10),
    },
    "ATP": {
        "round_1_wins": ("a player won a Round 1 match", 2),
        "round_2_wins": ("a player won a Round 2 match", 3),
        "round_3_wins": ("a player won a Round 3 match", 5),
        "round_4_wins": ("a player won a Round 4 match", 5),
        "quarterfinal_wins": ("a player won a Quarterfinal", 7),
        "semifinal_wins": ("a player won a Semifinal", 8),
        "final_wins": ("a player won the Final", 10),
    },
    "UCL": {
        "points": ("earned league-phase points", 3),
        "goal_differential": ("goal differential moved", 1),
    },
    # URC's compute_score rounds its final total to the nearest point
    # (confirmed: `return round(...)`), but these per-event deltas don't
    # individually round -- so a team's summed event points can land half
    # a point off compute_score's stored score. Same already-accepted
    # discrepancy compute_score_breakdown has for this exact league (its
    # own docstring: "Purely additive/independent of compute_score... a
    # bug here can never change an actual score, only its displayed
    # breakdown") -- not something to fix here either.
    "URC": {
        "table_points": ("earned table points", 2),
        "points_difference": ("points difference moved", 0.1),
    },
}
COUNT_EVENTS["WTA"] = COUNT_EVENTS["ATP"]

# league -> {stat key: (label, flat bonus)} for boolean achievement flags.
FLAG_EVENTS: dict[str, dict[str, tuple[str, float]]] = {
    "NFL": {
        "won_round1_or_bye": ("won/had a bye in the Wild Card round", 10),
        "won_round2": ("won the Divisional round", 20),
        "won_conf_champ": ("won the Conference Championship", 30),
        "won_sb": ("won the Super Bowl", 40),
    },
    "NBA": {
        "made_playoffs": ("clinched a playoff berth", 10),
        "won_round1": ("won Round 1", 10),
        "won_round2": ("won Round 2 (Conf. Semis)", 15),
        "won_conf_champ": ("won the Conference Championship", 25),
        "won_nba_champ": ("won the NBA Championship", 30),
    },
    "NHL": {
        "made_playoffs": ("clinched a playoff berth", 10),
        "won_round1": ("won Round 1", 10),
        "won_round2": ("won Round 2 (Conf. Semis)", 15),
        "won_conf_champ": ("won the Conference Championship", 25),
        "won_cup": ("won the Stanley Cup", 40),
    },
    "EPL": {},
    "NCAAF": {
        "playoff_bid": ("earned a CFP playoff bid", 10),
        "playoff_bye": ("received a playoff bye", 10),
        "championship_bid": ("reached the championship game", 20),
        "championship_win": ("won the championship", 30),
    },
    "ATP": {},
    "UCL": {
        "made_final_24": ("advanced to the knockout playoff round (top 24)", 10),
        "made_final_16": ("advanced to the Round of 16", 10),
        "made_final_8": ("advanced to the Quarterfinals", 10),
        "made_final_4": ("advanced to the Semifinals", 10),
        "made_final_2": ("advanced to the Final", 10),
        "won_final": ("won the Champions League", 10),
    },
    "URC": {
        "made_playoffs": ("clinched a playoff berth", 10),
        "won_quarterfinal": ("won the Quarterfinal", 15),
        "won_semifinal": ("won the Semifinal", 25),
        "won_final": ("won the Grand Final", 35),
    },
}
FLAG_EVENTS["WTA"] = FLAG_EVENTS["ATP"]


def diff_team_events(league: str, prev_stats: dict, curr_stats: dict) -> list[dict]:
    """Compares two consecutive days' stats for one team, returns
    [{"label": str, "points": float}] for everything that changed between
    them. Zero-point entries are dropped (same _nonzero convention
    league_rules.compute_score_breakdown already uses) -- an NHL OT/SO
    loss, for instance, is a real event but never worth showing in a feed
    about what's moving a team's score.

    For a team's first-ever TeamDailyScore row, pass
    season_labels.ZERO_STATS[league] as prev_stats so that day's full
    cumulative state (e.g. a team that already had playoff flags set by
    the time tracking started) surfaces as events too, not just day 2+."""
    events: list[dict] = []
    for key, (label, points_per_unit) in COUNT_EVENTS.get(league, {}).items():
        delta = curr_stats.get(key, 0) - prev_stats.get(key, 0)
        if delta:
            events.append({"label": f"{label} ({delta:+.0f})", "points": delta * points_per_unit})
    for key, (label, bonus) in FLAG_EVENTS.get(league, {}).items():
        if curr_stats.get(key) and not prev_stats.get(key):
            events.append({"label": label, "points": bonus})
    return [e for e in events if e["points"] != 0]
