"""Pulls today's schedule (or a given date) across all 7 in-scope
leagues from ESPN and writes it in the same shape as
data/daily-games/latest.json, for comparison against the current
manual/web-search-driven routine.

Run with: python3 fetch_schedule.py [YYYY-MM-DD]
"""
import json
import sys
from datetime import date

from espn_client import LEAGUE_ENDPOINTS, extract_games, fetch_scoreboard


def build_schedule(game_date: date) -> dict:
    games = []
    for league in LEAGUE_ENDPOINTS:
        raw = fetch_scoreboard(league, game_date)
        if "_error" in raw:
            print(f"  [{league}] ERROR: {raw['_error']}", file=sys.stderr)
            continue
        for g in extract_games(raw):
            games.append({"league": league, **g})
    return {"date": game_date.isoformat(), "games": games}


if __name__ == "__main__":
    target = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else date.today()
    result = build_schedule(target)
    out_path = f"output/schedule_{target.isoformat()}.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    by_league: dict[str, int] = {}
    for g in result["games"]:
        by_league[g["league"]] = by_league.get(g["league"], 0) + 1
    print(f"Wrote {len(result['games'])} game(s) for {target} -> {out_path}")
    for league, count in by_league.items():
        print(f"  {league}: {count}")
