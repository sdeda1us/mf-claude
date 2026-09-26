"""Nightly backup of every table in the database, emailed as a JSON
attachment to the commissioner.

Railway's own automated volume-backup feature would have been the
simpler fix here, but it's gated behind a paid plan this workspace isn't
on (confirmed against Railway's API: the write mutations for it come
back "Not Authorized" while the read-only ones succeed) -- hence this
app-level alternative instead.

Runs on an in-process schedule (see nightly_backup_loop, spawned from
main.py's lifespan) rather than a separate Railway cron service, so it
carries the same tradeoff already accepted elsewhere in this app for
turn/bid timers (auction_timer.py): it's in-memory and single-process,
so its countdown resets on every deploy/restart, and it would double-run
if this service were ever scaled past one replica. Neither is a concern
today (single replica, deploys aren't happening at 4 AM).

Only the commissioner receives the email, not every player -- the dump
includes CribSheetEntry, each user's private team valuations, which
would otherwise leak to every other player.

Can also be run on demand: `python -m app.backup` (e.g. via
`railway ssh -- python -m app.backup`, the same pattern already used by
app/seed_historical_results.py and app/set_ev_defaults.py for one-off
production commands).
"""
import asyncio
import json
import logging
from datetime import date, datetime, timedelta
from decimal import Decimal
from zoneinfo import ZoneInfo

from sqlalchemy import inspect as sa_inspect

from app.config import settings
from app.database import SessionLocal
from app.models import (
    Auction,
    AuctionItem,
    Bid,
    CribSheetEntry,
    QueueEntry,
    ReserveBid,
    RosterEntry,
    Season,
    Team,
    TeamSeasonResult,
    User,
    utcnow,
)
from app.slack_notify import notify_slack_sync

logger = logging.getLogger("megafantasy.backup")

EASTERN = ZoneInfo("America/New_York")
BACKUP_HOUR_ET = 4  # 4 AM Eastern -- well inside the existing 9 PM-9 AM quiet hours.

# Every table in the app, in FK-safe order (a table only appears after
# every table it references), so a restore can re-insert them back in
# this same order without violating a foreign key.
BACKUP_MODELS = [
    User,
    Season,
    Team,
    TeamSeasonResult,
    Auction,
    AuctionItem,
    Bid,
    ReserveBid,
    RosterEntry,
    QueueEntry,
    CribSheetEntry,
]


def _serialize(value):
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def _dump_table(db, model) -> list[dict]:
    columns = [c.key for c in sa_inspect(model).mapper.columns]
    return [
        {col: _serialize(getattr(obj, col)) for col in columns}
        for obj in db.query(model).all()
    ]


def build_backup_json() -> bytes:
    db = SessionLocal()
    try:
        payload = {
            "generated_at": utcnow().isoformat(),
            "tables": {model.__tablename__: _dump_table(db, model) for model in BACKUP_MODELS},
        }
    finally:
        db.close()
    return json.dumps(payload, indent=2).encode("utf-8")


def send_backup_email(payload: bytes) -> bool:
    """Returns True if an email was actually sent (vs. skipped because
    Resend or a commissioner isn't configured)."""
    if not settings.resend_api_key:
        logger.warning(
            "RESEND_API_KEY not set -- skipping nightly backup email (payload was %d bytes)",
            len(payload),
        )
        return False

    db = SessionLocal()
    try:
        commissioner = db.query(User).filter(User.is_commissioner.is_(True)).first()
    finally:
        db.close()
    if commissioner is None:
        logger.warning("No commissioner user found -- skipping nightly backup email")
        return False

    import resend

    resend.api_key = settings.resend_api_key
    today = date.today().isoformat()
    resend.Emails.send(
        {
            "from": settings.email_from,
            "to": [commissioner.email],
            "subject": f"Megafantasy backup — {today}",
            "html": (
                "<p>Attached: a full JSON export of every Megafantasy table, "
                "generated tonight. Keep it somewhere safe (not required "
                "reading -- just a disaster-recovery copy).</p>"
            ),
            "attachments": [
                {"filename": f"megafantasy-backup-{today}.json", "content": list(payload)}
            ],
        }
    )
    return True


def run_backup() -> None:
    payload = build_backup_json()
    sent = send_backup_email(payload)
    status = f"emailed ({len(payload)} bytes)" if sent else f"skipped (see logs), {len(payload)} bytes generated"
    logger.info("Nightly backup: %s", status)
    # No Slack ping on success -- the email landing in the commissioner's
    # inbox each night is already the positive signal; Slack is reserved
    # for the one case that actually needs attention.
    if not sent:
        notify_slack_sync(f"🗄️ Nightly backup did not send an email: {status}")


def _seconds_until_next_run(now: datetime | None = None) -> float:
    now_et = (now or datetime.now(EASTERN)).astimezone(EASTERN)
    target = now_et.replace(hour=BACKUP_HOUR_ET, minute=0, second=0, microsecond=0)
    if target <= now_et:
        target += timedelta(days=1)
    return (target - now_et).total_seconds()


async def nightly_backup_loop() -> None:
    """Runs forever: sleeps until the next 4 AM Eastern, backs up, repeats.
    Spawned once from main.py's lifespan. A failed attempt is logged and
    reported to Slack but never crashes the loop -- there's always a next
    night to try again."""
    while True:
        await asyncio.sleep(_seconds_until_next_run())
        try:
            await asyncio.to_thread(run_backup)
        except Exception:
            logger.exception("Nightly backup failed")
            notify_slack_sync("🗄️ Nightly backup FAILED -- check the backend logs.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_backup()
