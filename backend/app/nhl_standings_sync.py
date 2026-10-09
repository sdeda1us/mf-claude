"""Syncs NHL standings directly from the NHL's own public data API, run
from this backend process rather than the scheduled Claude Code routine
(see daily_sync_pull.py's module docstring for why that routine exists at
all: it runs in a sandboxed cloud environment with heavily restricted
outbound network access). That routine's own egress proxy rejects
essentially every external site it has tried, api-web.nhle.com included
(confirmed: a direct curl from inside that sandbox came back
"connect_rejected"), so WebSearch was the only option left for NHL --
and WebSearch alone can't reliably surface the regulation-win/OT-win
split league_rules.compute_score needs for NHL, so two routine runs
skipped NHL for lack of it and a third guessed at it from contradictory
search snippets.

This backend (an ordinary Railway service with normal, unrestricted
outbound internet access -- same reasoning as daily_sync_pull.py's own
GitHub pull) can just fetch the authoritative source itself, so NHL no
longer depends on the routine's sandbox or WebSearch at all. Run
alongside daily_sync_pull.py's other pulls, from the same in-process
schedule (see daily_sync_pull_loop) -- same tradeoffs apply (in-memory,
resets on deploy/restart; idempotent per real-world day, so a double-run
is harmless).

Can also be run on demand: `python -m app.nhl_standings_sync`
"""
import logging
from datetime import date

import requests

from app.daily_score_sync import apply_daily_sync_batch, today_eastern
from app.database import SessionLocal
from app.schemas import DailySyncEntryIn

logger = logging.getLogger("megafantasy.nhl_standings_sync")

STANDINGS_URL = "https://api-web.nhle.com/v1/standings/{date}"

# The only team name mismatch between this API and the app's Team rows
# (confirmed by diffing all 32 names) -- the API spells this one with the
# accent, CLAUDE.md/the app's Team row does not.
NAME_FIXUPS = {"Montréal Canadiens": "Montreal Canadiens"}


def fetch_nhl_standings(as_of: date | None = None) -> list[DailySyncEntryIn]:
    """as_of defaults to today (Eastern) -- the API returns standings as of
    games completed through that date, which is exactly "through
    yesterday's games" when called before today's games have been played,
    same convention every other league's sync already uses."""
    as_of = as_of or today_eastern()
    resp = requests.get(
        STANDINGS_URL.format(date=as_of.isoformat()),
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )
    resp.raise_for_status()
    payload = resp.json()

    entries = []
    for team in payload["standings"]:
        name = team["teamName"]["default"]
        name = NAME_FIXUPS.get(name, name)
        reg_wins = team["regulationWins"]
        stats = {
            "reg_wins": reg_wins,
            "reg_losses": team["losses"],
            "ot_so_wins": team["regulationPlusOtWins"] - reg_wins,
            "made_playoffs": False,
            "won_round1": False,
            "won_round2": False,
            "won_conf_champ": False,
            "won_cup": False,
        }
        entries.append(DailySyncEntryIn(league="NHL", team=name, stats=stats))
    return entries


def sync_nhl_standings() -> dict:
    entries = fetch_nhl_standings()
    db = SessionLocal()
    try:
        result = apply_daily_sync_batch(db, entries)
        db.commit()
    finally:
        db.close()
    return {"synced": result.synced, "skipped": [s.model_dump() for s in result.skipped]}


if __name__ == "__main__":
    import json

    logging.basicConfig(level=logging.INFO)
    print(json.dumps(sync_nhl_standings(), indent=2))
