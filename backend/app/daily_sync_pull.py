"""Pulls the day's researched stats from a JSON file the scheduled Claude
Code routine commits to this repo, and ingests it through the same logic
POST /api/scoring-sync/batch uses.

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
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import requests

from app.daily_games_sync import sync_games_for_date
from app.daily_results_sync import sync_results_for_date
from app.daily_score_sync import NoActiveSeasonError, apply_daily_sync_batch
from app.database import SessionLocal
from app.schemas import DailyGameEntryIn, DailyResultEntryIn, DailySyncEntryIn
from app.slack_notify import notify_slack_sync

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
GAMES_RAW_URL = "https://raw.githubusercontent.com/sdeda1us/mf-claude/main/data/daily-games/latest.json"
RESULTS_RAW_URL = "https://raw.githubusercontent.com/sdeda1us/mf-claude/main/data/daily-results/latest.json"


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


def pull_and_sync_games() -> dict:
    """Same pull-from-GitHub pattern as pull_and_sync, for the Home
    page's "Today's Games" widget. A null `date` in the payload (the
    repo's placeholder data/daily-games/latest.json, shipped before the
    routine is updated to populate it for real) is a harmless no-op, not
    an error."""
    response = requests.get(GAMES_RAW_URL, timeout=30)
    response.raise_for_status()
    payload = response.json()
    if not payload.get("date"):
        return {"synced": 0, "date": None}
    game_date = date.fromisoformat(payload["date"])
    entries = [DailyGameEntryIn(**g) for g in payload.get("games", [])]

    db = SessionLocal()
    try:
        count = sync_games_for_date(db, game_date, entries)
        db.commit()
    finally:
        db.close()
    return {"synced": count, "date": payload["date"]}


def pull_and_sync_results() -> dict:
    """Same pull-from-GitHub pattern as pull_and_sync_games, for the Home
    page's "Yesterday's Results" card. A null `date` (no routine run has
    populated this file yet, or yesterday had nothing to report) is a
    harmless no-op, not an error."""
    response = requests.get(RESULTS_RAW_URL, timeout=30)
    response.raise_for_status()
    payload = response.json()
    if not payload.get("date"):
        return {"updated": 0, "date": None}
    result_date = date.fromisoformat(payload["date"])
    entries = [DailyResultEntryIn(**r) for r in payload.get("results", [])]

    db = SessionLocal()
    try:
        result = sync_results_for_date(db, result_date, entries)
        db.commit()
    finally:
        db.close()
    return {"updated": result["updated"], "skipped": result["skipped"], "date": payload["date"]}


async def _run_score_pull_and_report(context: str) -> None:
    try:
        result = await asyncio.to_thread(pull_and_sync)
        logger.info("Daily sync pull (%s): %s", context, result)
        if result["skipped"]:
            notify_slack_sync(
                f"📊 Daily score sync ({context}): {result['synced']} synced, "
                f"{len(result['skipped'])} skipped -- check logs for details."
            )
    except NoActiveSeasonError:
        logger.warning("Daily sync pull (%s): no active season, skipping", context)
    except Exception:
        logger.exception("Daily sync pull (%s) failed", context)
        notify_slack_sync(f"📊 Daily score sync ({context}) FAILED -- check the backend logs.")


async def _run_games_pull_and_report(context: str) -> None:
    """Separate from _run_score_pull_and_report so a games-pull failure
    (including a missing/malformed file before the routine is updated to
    produce one) never blocks or gets conflated with the score pull's own
    reporting -- that one stays the higher-urgency signal."""
    try:
        result = await asyncio.to_thread(pull_and_sync_games)
        logger.info("Daily games pull (%s): %s", context, result)
    except Exception:
        logger.exception("Daily games pull (%s) failed", context)
        notify_slack_sync(f"🗓️ Daily games sync ({context}) failed -- check the backend logs.")


async def _run_results_pull_and_report(context: str) -> None:
    """Separate from the other two pulls for the same isolation reason
    _run_games_pull_and_report is -- a results-pull failure (including a
    missing/malformed file before the routine is updated to produce one)
    never blocks or gets conflated with the score pull's own reporting."""
    try:
        result = await asyncio.to_thread(pull_and_sync_results)
        logger.info("Daily results pull (%s): %s", context, result)
        if result.get("skipped"):
            notify_slack_sync(
                f"🏁 Daily results sync ({context}): {result['updated']} updated, "
                f"{len(result['skipped'])} had no matching scheduled game -- check logs."
            )
    except Exception:
        logger.exception("Daily results pull (%s) failed", context)
        notify_slack_sync(f"🏁 Daily results sync ({context}) failed -- check the backend logs.")


async def _run_pull_and_report(context: str) -> None:
    await _run_score_pull_and_report(context)
    await _run_games_pull_and_report(context)
    await _run_results_pull_and_report(context)


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

    A failed attempt is logged and reported to Slack but never crashes the
    loop -- there's always a next day to try again."""
    if _todays_run_already_passed():
        await _run_pull_and_report("startup catch-up")

    while True:
        await asyncio.sleep(_seconds_until_next_run())
        await _run_pull_and_report("scheduled")


if __name__ == "__main__":
    print(pull_and_sync())
    print(pull_and_sync_games())
    print(pull_and_sync_results())
