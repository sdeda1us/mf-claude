"""Minimal client for ESPN's unofficial/undocumented "site API" --
exploratory experiment only.

No API key, no auth, no published SLA or rate-limit docs -- this is the
same JSON ESPN's own site/app calls under the hood, reverse-engineered
from public endpoint patterns. Covers exactly the 7 leagues in scope for
Megafantasy's "Today's Games" / "Yesterday's Results" widgets (see
backend/app/routers/seasons.py's TODAYS_GAMES_LEAGUES and
data/daily-games/README.md): NFL, NBA, NHL, EPL, UCL, URC, NCAAF.
"""
import json
import urllib.error
import urllib.request
from datetime import date

BASE = "https://site.api.espn.com/apis/site/v2/sports"

# Megafantasy league code -> (ESPN scoreboard URL path, extra query params).
# NCAAF: groups=80 scopes to FBS (matches CLAUDE.md's 138-team FBS-only
# pool); limit=500 overrides ESPN's default page size of ~30 so a full
# Saturday slate doesn't get truncated.
LEAGUE_ENDPOINTS = {
    "NFL": ("football/nfl", {}),
    "NBA": ("basketball/nba", {}),
    "NHL": ("hockey/nhl", {}),
    "EPL": ("soccer/eng.1", {}),
    "UCL": ("soccer/uefa.champions", {}),
    "URC": ("rugby/270557", {}),
    "NCAAF": ("football/college-football", {"groups": "80", "limit": "500"}),
}


def fetch_scoreboard(league: str, game_date: date | None = None, timeout: int = 10) -> dict:
    """Raw scoreboard JSON for one league. game_date=None means "ESPN's
    default" (today, in US/Eastern-ish terms as ESPN defines it)."""
    path, extra = LEAGUE_ENDPOINTS[league]
    params = dict(extra)
    if game_date is not None:
        params["dates"] = game_date.strftime("%Y%m%d")
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{BASE}/{path}/scoreboard"
    if qs:
        url += f"?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read())
    except urllib.error.URLError as exc:
        return {"_error": str(exc)}


def extract_games(raw: dict) -> list[dict]:
    """Normalizes one league's scoreboard response into Megafantasy's
    shape: {league, home_team, away_team, venue, time_label, home_score,
    away_score, status}. Score fields are None pre-kickoff. `status` is
    extra (not in the production JSON shape) -- kept here to show what
    ESPN exposes for in-progress/postponed games that the current
    fixture format has no slot for."""
    games = []
    for event in raw.get("events", []):
        comp = event["competitions"][0]
        home = next(c for c in comp["competitors"] if c["homeAway"] == "home")
        away = next(c for c in comp["competitors"] if c["homeAway"] == "away")
        status = event.get("status", {}).get("type", {})
        venue = comp.get("venue", {}).get("fullName")
        games.append(
            {
                "home_team": home["team"]["displayName"],
                "away_team": away["team"]["displayName"],
                "venue": venue,
                "time_label": event.get("date"),
                "home_score": int(home["score"]) if status.get("completed") else None,
                "away_score": int(away["score"]) if status.get("completed") else None,
                "status": status.get("description"),
            }
        )
    return games
