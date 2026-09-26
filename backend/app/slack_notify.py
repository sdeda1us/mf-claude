"""Posts live auction activity to a Slack channel via an Incoming Webhook
(https://api.slack.com/messaging/webhooks) — no bot to invite, no OAuth
scopes, just a per-channel URL pasted into SLACK_WEBHOOK_URL.

notify_slack() spawns its own background task (via the same
manager.spawn() this app already uses for timer tasks) that runs the
actual network request in a worker thread, so a slow or unreachable
Slack endpoint never adds latency to a bid, nomination, or sale — call
sites just call it and move on. Same "gracefully do nothing if
unconfigured" spirit as app/email.py: no SLACK_WEBHOOK_URL set, no
requests ever go out, and nothing else about the app changes.
"""
import asyncio
import logging

import requests
from sqlalchemy.orm import Session

from app.config import settings
from app.models import AuctionItem, User
from app.ws.connection_manager import manager

logger = logging.getLogger("megafantasy.slack")


def _post(text: str) -> None:
    if not settings.slack_webhook_url:
        return
    try:
        requests.post(settings.slack_webhook_url, json={"text": text}, timeout=5)
    except Exception:
        # A Slack outage/misconfigured URL should never take down the
        # auction it's just reporting on.
        logger.exception("Failed to post Slack notification")


def notify_slack(text: str) -> None:
    """Fire-and-forget: schedules `text` to be posted in the background.
    Safe to call from anywhere already inside a running event loop
    (every call site here is)."""
    manager.spawn(asyncio.to_thread(_post, text))


def notify_slack_sync(text: str) -> None:
    """Same as notify_slack, but posts inline instead of scheduling a
    task — for callers with no running event loop to schedule onto (e.g.
    app/backup.py's run_backup, which is also invoked standalone via
    `python -m app.backup`). Already blocking-safe on its own (same `_post`,
    same short timeout), so there's nothing to gain from backgrounding it
    outside of an event loop context anyway."""
    _post(text)


def _display_name(db: Session, user_id: int) -> str:
    user = db.get(User, user_id)
    return user.display_name if user is not None else f"User #{user_id}"


def notify_nomination(nominator_name: str, team_name: str, league: str) -> None:
    notify_slack(f"📣 *{nominator_name}* nominated *{team_name}* ({league}) — bidding is open!")


def notify_auto_nomination(db: Session, idle_user_id: int, team_name: str, league: str, opening_amount: float) -> None:
    name = _display_name(db, idle_user_id)
    notify_slack(
        f"⏰ *{name}*'s turn timed out — *{team_name}* ({league}) was auto-nominated on their "
        f"behalf (opening bid ${opening_amount:.0f})."
    )


def notify_bid(bidder_name: str, team_name: str, league: str, amount: float, *, via_reserve: bool = False) -> None:
    suffix = " (reserve auto-bid)" if via_reserve else ""
    notify_slack(f"💰 *{bidder_name}* bid *${amount:.0f}* on *{team_name}* ({league}){suffix}.")


def notify_reserve_bid_cascade(db: Session, item: AuctionItem, placed: list[tuple[int, float]]) -> None:
    """One notification per reserve auto-bid `resolve_reserve_bids` placed
    (in order) — that function can't post these itself (it can't import
    the manager.spawn used above without a circular import back to
    itself), so it just returns what it did and callers report it."""
    for user_id, amount in placed:
        notify_bid(_display_name(db, user_id), item.team.name, item.team.league, amount, via_reserve=True)


def notify_sold(db: Session, item: AuctionItem) -> None:
    if item.winning_user_id is None:
        notify_slack(f"📭 *{item.team.name}* ({item.team.league}) went unsold — no bids.")
        return
    winner_name = _display_name(db, item.winning_user_id)
    notify_slack(
        f"🏆 *{item.team.name}* ({item.team.league}) SOLD to *{winner_name}* for "
        f"*${float(item.winning_bid):.0f}*!"
    )
