"""Pulls the day's researched team stats from a JSON file the scheduled
Claude Code routine commits to this repo, and ingests it through the
same logic POST /api/scoring-sync/batch uses.

Why pull instead of the routine pushing directly: the routine runs inside
a sandboxed cloud environment whose outbound network access is restricted
to a small fixed allowlist (Anthropic's own APIs, package registries) --
it cannot reach megafantasy.win at all (confirmed: a direct POST attempt
was rejected by the sandbox's own egress proxy with a 403). It CAN push
to GitHub (a different path than the HTTPS egress proxy, since it already
clones this repo over git to read season_labels.py/docs/wiki/CLAUDE.md),
so instead it commits the day's batch to data/daily-sync/latest.json on
main. This backend process -- an ordinary Railway service with normal,
unrestricted outbound internet access, unlike the sandbox -- pulls that
file on its own schedule instead.

Today's games / yesterday's results used to follow this same
routine-commits-a-file/backend-pulls-it pattern (data/daily-games/,
data/daily-results/), but those two now sync directly from ESPN's API
instead -- see espn_games_sync.py / espn_results_sync.py and
espn_client.py's module docstring. Same reasoning as nhl_standings_sync.py
already bypassing the routine for NHL standings: an espn_test/ experiment
found the routine's sandbox (and even the WebFetch tool) can't reach
ESPN's API at all, while this backend -- unrestricted egress, same as the
GitHub pull below -- can just fetch it directly, with far better
completeness than the routine's web-search step ever had (confirmed by
diffing a day's worth of output: the routine's committed files were
missing roughly 40% of that day's games/results, all cases where ESPN's
API had them correctly). data/daily-games/ and data/daily-results/ are
no longer read by anything; the routine does not need to populate them.

The repo is public, so this is an unauthenticated GET against GitHub's
raw-content host -- no token needed.

Runs on an in-process schedule (see daily_sync_pull_loop, spawned from
main.py's lifespan), same tradeoff already accepted for backup.py /
auction_timer.py: in-memory, resets on deploy/restart, would double-run
if this service were ever scaled past one replica. Pulling the same
unchanged file twice is harmless -- app.daily_score_sync's sync is
idempotent per real-world day.

Can also be run on demand: `python -m app.daily_sync_pull`
"""
import asyncio
import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests

from app.daily_score_sync import NoActiveSeasonError, apply_daily_sync_batch
from app.database import SessionLocal
from app.espn_epl_standings_sync import sync_epl_standings
from app.espn_games_sync import sync_espn_games
from app.espn_nba_standings_sync import sync_nba_standings
from app.espn_ncaaf_standings_sync import sync_ncaaf_standings
from app.espn_nfl_standings_sync import sync_nfl_standings
from app.espn_results_sync import sync_espn_results
from app.espn_ucl_standings_sync import sync_ucl_standings
from app.espn_urc_standings_sync import sync_urc_standings
from app.nhl_standings_sync import sync_nhl_standings
from app.schemas import DailySyncEntryIn

logger = logging.getLogger("megafantasy.daily_sync_pull")

EASTERN = ZoneInfo("America/New_York")
# 30 minutes after the routine's 4:30am Central (5:30am Eastern) run --
# tight (the routine itself typically takes ~15-20 min), but intentional:
# showing fresh data sooner was worth the risk of an occasional slow run
# getting picked up a day late instead of same-day. A day-late pickup is
# still harmless/idempotent (see daily_sync_pull_loop's docstring below),
# just not what today's visitors will see.
PULL_HOUR_ET = 6

RAW_URL = "https://raw.githubusercontent.com/sdeda1us/mf-claude/main/data/daily-sync/latest.json"


def _seconds_until_next_run(now: datetime | None = None) -> float:
    now_et = (now or datetime.now(EASTERN)).astimezone(EASTERN)
    target = now_et.replace(hour=PULL_HOUR_ET, minute=0, second=0, microsecond=0)
    if target <= now_et:
        target += timedelta(days=1)
    return (target - now_et).total_seconds()


def _todays_run_already_passed(now: datetime | None = None) -> bool:
    now_et = (now or datetime.now(EASTERN)).astimezone(EASTERN)
    todays_target = now_et.replace(hour=PULL_HOUR_ET, minute=0, second=0, microsecond=0)
    return now_et >= todays_target


def pull_and_sync() -> dict:
    response = requests.get(RAW_URL, timeout=30)
    response.raise_for_status()
    payload = response.json()
    entries = [DailySyncEntryIn(**e) for e in payload.get("entries", [])]

    db = SessionLocal()
    try:
        result = apply_daily_sync_batch(db, entries)
        db.commit()
    finally:
        db.close()
    return {"synced": result.synced, "skipped": [s.model_dump() for s in result.skipped]}


async def _run_score_pull_and_report(context: str) -> None:
    try:
        result = await asyncio.to_thread(pull_and_sync)
        logger.info("Daily sync pull (%s): %s", context, result)
    except NoActiveSeasonError:
        logger.warning("Daily sync pull (%s): no active season, skipping", context)
    except Exception:
        logger.exception("Daily sync pull (%s) failed", context)


async def _run_espn_games_and_report(context: str) -> None:
    """Fetches today's schedule straight from ESPN -- see
    espn_games_sync.py / espn_client.py's module docstrings. Separate from
    _run_score_pull_and_report so a failure here (including ESPN being
    unreachable or changing its response shape) never blocks or gets
    conflated with the score pull's own reporting -- that one stays the
    higher-urgency signal."""
    try:
        result = await asyncio.to_thread(sync_espn_games)
        logger.info("ESPN games sync (%s): %s", context, result)
    except Exception:
        logger.exception("ESPN games sync (%s) failed", context)


async def _run_espn_results_and_report(context: str) -> None:
    """Fetches yesterday's final scores straight from ESPN -- see
    espn_results_sync.py / espn_client.py's module docstrings. Separate
    from the other pulls for the same isolation reason
    _run_espn_games_and_report is."""
    try:
        result = await asyncio.to_thread(sync_espn_results)
        logger.info("ESPN results sync (%s): %s", context, result)
    except Exception:
        logger.exception("ESPN results sync (%s) failed", context)


async def _run_standings_sync_and_report(context: str, log_label: str, emoji: str, sync_fn) -> None:
    """Shared wrapper for every ESPN-direct standings sync (NHL, NBA,
    NFL, NCAAF, EPL, UCL, URC -- each a {"synced": int, "skipped": [...]}
    result, same shape pull_and_sync's GitHub-sourced batch returns).
    Extracted once there were 7 near-identical copies of this -- see each
    sync module's own docstring for why that league bypasses the routine.
    Isolates one league's failure from the rest, same reasoning as the
    other _run_*_and_report wrappers: a failure here never blocks or gets
    conflated with another sync's reporting."""
    try:
        result = await asyncio.to_thread(sync_fn)
        logger.info("%s (%s): %s", log_label, context, result)
    except NoActiveSeasonError:
        logger.warning("%s (%s): no active season, skipping", log_label, context)
    except Exception:
        logger.exception("%s (%s) failed", log_label, context)


async def _run_pull_and_report(context: str) -> None:
    await _run_score_pull_and_report(context)
    await _run_standings_sync_and_report(context, "NHL standings sync", "🏒", sync_nhl_standings)
    await _run_standings_sync_and_report(context, "NFL standings sync", "🏈", sync_nfl_standings)
    await _run_standings_sync_and_report(context, "NBA standings sync", "🏀", sync_nba_standings)
    await _run_standings_sync_and_report(context, "NCAAF standings sync", "🏈", sync_ncaaf_standings)
    await _run_standings_sync_and_report(context, "EPL standings sync", "⚽", sync_epl_standings)
    await _run_standings_sync_and_report(context, "UCL standings sync", "⚽", sync_ucl_standings)
    await _run_standings_sync_and_report(context, "URC standings sync", "🏉", sync_urc_standings)
    await _run_espn_games_and_report(context)
    await _run_espn_results_and_report(context)


async def daily_sync_pull_loop() -> None:
    """Runs forever: sleeps until the next PULL_HOUR_ET (Eastern), pulls and
    ingests, repeats. Spawned once from main.py's lifespan.

    Also catches up immediately on startup if today's pull hour has already
    passed -- otherwise today gets silently skipped entirely, since the
    sleep loop below would just compute "next run = tomorrow" with no
    record today was ever missed. This happened for real on 2026-10-04
    (back when PULL_HOUR_ET was 9): the first deploy that day landed at
    11:49am ET, well past that day's pull hour, and nothing caught it up
    until the following day's scheduled run
    -- the whole day has zero TeamDailyScore rows as a result. Re-pulling a
    day that already got its scheduled sync is harmless (idempotent per
    real-world day, see module docstring), so this runs unconditionally
    whenever we're past today's hour rather than first checking whether
    today's scheduled pull actually happened.

    A failed attempt is logged (Railway's log stream, not Slack -- see
    _run_*_and_report above) but never crashes the loop -- there's always
    a next day to try again."""
    if _todays_run_already_passed():
        await _run_pull_and_report("startup catch-up")

    while True:
        await asyncio.sleep(_seconds_until_next_run())
        await _run_pull_and_report("scheduled")


if __name__ == "__main__":
    print(pull_and_sync())
    print(sync_nhl_standings())
    print(sync_nfl_standings())
    print(sync_nba_standings())
    print(sync_ncaaf_standings())
    print(sync_epl_standings())
    print(sync_ucl_standings())
    print(sync_urc_standings())
    print(sync_espn_games())
    print(sync_espn_results())
