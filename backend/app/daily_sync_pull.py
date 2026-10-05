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
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import requests

from app.daily_score_sync import NoActiveSeasonError, apply_daily_sync_batch
from app.database import SessionLocal
from app.schemas import DailySyncEntryIn
from app.slack_notify import notify_slack_sync

logger = logging.getLogger("megafantasy.daily_sync_pull")

EASTERN = ZoneInfo("America/New_York")
# An hour after the routine's 7am Central (8am Eastern) run, to leave it
# room to finish researching and pushing before this pulls.
PULL_HOUR_ET = 9

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


async def _run_pull_and_report(context: str) -> None:
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


async def daily_sync_pull_loop() -> None:
    """Runs forever: sleeps until the next 9 AM Eastern, pulls and ingests,
    repeats. Spawned once from main.py's lifespan.

    Also catches up immediately on startup if today's 9 AM Eastern slot has
    already passed -- otherwise today gets silently skipped entirely, since
    the sleep loop below would just compute "next run = tomorrow" with no
    record today was ever missed. This happened for real on 2026-10-04: the
    first deploy that day landed at 11:49am ET, well past the 9am pull
    hour, and nothing caught it up until the following day's scheduled run
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
