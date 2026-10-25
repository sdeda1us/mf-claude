"""Pulls final scores for a given date (default: yesterday) across all
7 in-scope leagues from ESPN and writes it in the same shape as
data/daily-results/latest.json.

Run with: python3 fetch_results.py [YYYY-MM-DD]
"""
import json
import sys
from datetime import date, timedelta

from espn_client import LEAGUE_ENDPOINTS, extract_games, fetch_scoreboard


def build_results(game_date: date) -> dict:
    results = []
    for league in LEAGUE_ENDPOINTS:
        raw = fetch_scoreboard(league, game_date)
        if "_error" in raw:
            print(f"  [{league}] ERROR: {raw['_error']}", file=sys.stderr)
            continue
        for g in extract_games(raw):
            if g["home_score"] is None:
                continue  # not completed -- nothing to report yet
            results.append(
                {
                    "league": league,
                    "home_team": g["home_team"],
                    "away_team": g["away_team"],
                    "home_score": g["home_score"],
                    "away_score": g["away_score"],
                }
            )
    return {"date": game_date.isoformat(), "results": results}


if __name__ == "__main__":
    target = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else date.today() - timedelta(days=1)
    result = build_results(target)
    out_path = f"output/results_{target.isoformat()}.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    by_league: dict[str, int] = {}
    for r in result["results"]:
        by_league[r["league"]] = by_league.get(r["league"], 0) + 1
    print(f"Wrote {len(result['results'])} result(s) for {target} -> {out_path}")
    for league, count in by_league.items():
        print(f"  {league}: {count}")
