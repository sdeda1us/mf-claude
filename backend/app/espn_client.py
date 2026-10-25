"""Shared client for ESPN's public (unofficial, undocumented) scoreboard
API -- used by espn_games_sync.py and espn_results_sync.py to fetch
today's schedule / yesterday's results directly from this backend
process, the same way nhl_standings_sync.py fetches NHL standings
directly rather than depending on the scheduled Claude Code routine (see
that module's docstring for why: the routine's sandbox rejects direct
calls to most external hosts, ESPN's included -- confirmed by a one-off
espn_test/ experiment where even the WebFetch tool got a 403 against
this same API).

No API key or auth; no published SLA or rate-limit docs. Scoped to the
7 leagues in TODAYS_GAMES_LEAGUES (backend/app/routers/seasons.py):
NFL, NBA, NHL, EPL, UCL, URC, NCAAF.
"""
from datetime import date, datetime
from zoneinfo import ZoneInfo

import requests

BASE = "https://site.api.espn.com/apis/site/v2/sports"
STANDINGS_BASE = "https://site.api.espn.com/apis/v2/sports"
EASTERN = ZoneInfo("America/New_York")

# Standings-capable leagues -> (sport path, extra query params), used by
# the espn_*_standings_sync modules (NFL/NCAAF/UCL/URC -- NBA and EPL
# hardcode their own URL in their own sync module since they predate this
# shared helper; NHL comes from the NHL's own API, not ESPN, see
# nhl_standings_sync.py). Same sport paths as LEAGUE_ENDPOINTS above, just
# a different ESPN API surface (v2/.../standings instead of
# site/v2/.../scoreboard).
STANDINGS_ENDPOINTS = {
    "NFL": ("football/nfl", {}),
    "UCL": ("soccer/uefa.champions", {}),
    "URC": ("rugby/270557", {}),
    "NCAAF": ("football/college-football", {}),
}

# Megafantasy league code -> (ESPN scoreboard URL path, extra query params).
# NCAAF: groups=80 scopes to FBS (matches CLAUDE.md's 138-team FBS-only
# pool); limit=500 overrides ESPN's default page size so a full Saturday
# slate doesn't get truncated. URC's path is a numeric ESPN league id
# (270557) rather than a slug -- found by walking
# sports.core.api.espn.com/v2/sports/rugby/leagues and checking names,
# since ESPN has no human-readable slug for it the way soccer leagues do.
LEAGUE_ENDPOINTS = {
    "NFL": ("football/nfl", {}),
    "NBA": ("basketball/nba", {}),
    "NHL": ("hockey/nhl", {}),
    "EPL": ("soccer/eng.1", {}),
    "UCL": ("soccer/uefa.champions", {}),
    "URC": ("rugby/270557", {}),
    "NCAAF": ("football/college-football", {"groups": "80", "limit": "500"}),
}


def fetch_scoreboard(league: str, game_date: date | None = None, timeout: int = 30) -> dict:
    """Raw scoreboard JSON for one league. game_date=None means "ESPN's
    default" (today)."""
    path, extra = LEAGUE_ENDPOINTS[league]
    params = dict(extra)
    if game_date is not None:
        params["dates"] = game_date.strftime("%Y%m%d")
    resp = requests.get(
        f"{BASE}/{path}/scoreboard",
        params=params,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()


def fetch_standings(league: str, timeout: int = 30) -> dict:
    """Raw standings JSON for one league (current season, current state --
    no historical-date parameter the way scoreboard has)."""
    path, extra = STANDINGS_ENDPOINTS[league]
    resp = requests.get(
        f"{STANDINGS_BASE}/{path}/standings",
        params=extra,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()


def flatten_standings_entries(node: dict) -> list[dict]:
    """ESPN nests standings by conference/division to an inconsistent
    depth -- most conferences carry entries directly, but at least one
    (NCAAF's Sun Belt) nests an extra "children" level for divisions
    instead. Recursing through every "children" list and collecting each
    node's "standings.entries" handles both shapes (and however deep a
    future league nests) without needing to special-case which leagues
    have divisions."""
    entries = list(node.get("standings", {}).get("entries", []))
    for child in node.get("children", []):
        entries.extend(flatten_standings_entries(child))
    return entries


def _format_time_label(iso_date: str) -> str:
    """"2026-10-25T13:30Z" -> "9:30 AM ET", matching the time_label style
    the routine's fixtures already use."""
    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00")).astimezone(EASTERN)
    return dt.strftime("%-I:%M %p ET")


def extract_games(raw: dict) -> list[dict]:
    """Normalizes one league's scoreboard response into {home_team,
    away_team, venue, time_label, home_score, away_score} -- team names
    are ESPN's raw displayName, not yet canonicalized against seed.py
    (callers should run these through team_name_aliases.canonicalize_team_name).
    Score fields are None for a game that hasn't finished."""
    games = []
    for event in raw.get("events", []):
        comp = event["competitions"][0]
        home = next(c for c in comp["competitors"] if c["homeAway"] == "home")
        away = next(c for c in comp["competitors"] if c["homeAway"] == "away")
        completed = event.get("status", {}).get("type", {}).get("completed", False)
        games.append(
            {
                "home_team": home["team"]["displayName"],
                "away_team": away["team"]["displayName"],
                "venue": comp.get("venue", {}).get("fullName"),
                "time_label": _format_time_label(event["date"]) if event.get("date") else None,
                "home_score": int(home["score"]) if completed else None,
                "away_score": int(away["score"]) if completed else None,
            }
        )
    return games
