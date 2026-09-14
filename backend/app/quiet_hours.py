"""Auction timers observe a nightly "quiet hours" window, 9 PM-9 AM
Eastern, during which no deadline is allowed to expire -- nobody's
nomination turn times out into an auto-nomination, and no active item's
bidding window closes on its own. Players can still bid, pass, and set
reserves as usual through the night; only the automatic, clock-driven
actions pause.

The mechanism: every timeout this app hands out (the nomination-turn
timeout, the bid window, the soft-close bid extension) is computed as "N
seconds of active time from now" via add_active_duration() below, instead
of a flat "N seconds from now" -- it walks forward from a start time and
skips over any quiet-hours window it crosses, so the deadline it returns
always lands in daytime. Because that math runs once, at the moment a
deadline is set, rather than depending on some ongoing pause/resume
state, it's automatically robust to server restarts: recomputing from the
same stored start time (e.g. Auction.turn_started_at) always yields the
same deadline, no separate "are we currently paused for the night" flag
to track or re-arm.

No third-party tz data dependency risk: America/New_York needs the IANA
tzdata database, which isn't guaranteed to ship inside every minimal
Linux container image (unlike this dev machine) -- see the `tzdata`
package in requirements.txt, which zoneinfo falls back to automatically
when the OS doesn't have its own copy.
"""
from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

EASTERN = ZoneInfo("America/New_York")
QUIET_START = time(21, 0)  # 9 PM Eastern
QUIET_END = time(9, 0)  # 9 AM Eastern


def _naive_utc(dt: datetime) -> datetime:
    # Mirrors auction_timer.naive_utc / auction_service._naive_utc
    # (duplicated rather than imported to keep this module dependency-free
    # and avoid any risk of a circular import, same reasoning as those).
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def _to_eastern(dt: datetime) -> datetime:
    return _naive_utc(dt).replace(tzinfo=timezone.utc).astimezone(EASTERN)


def _to_utc_naive(dt_eastern: datetime) -> datetime:
    return dt_eastern.astimezone(timezone.utc).replace(tzinfo=None)


def _is_quiet_eastern(dt_eastern: datetime) -> bool:
    t = dt_eastern.time()
    return t >= QUIET_START or t < QUIET_END


def is_quiet_hours(dt: datetime | None = None) -> bool:
    """True if the given moment (aware or naive UTC; defaults to now)
    falls in the 9 PM-9 AM Eastern quiet window."""
    return _is_quiet_eastern(_to_eastern(dt if dt is not None else datetime.utcnow()))


def _next_transition(dt_eastern: datetime) -> datetime:
    """The next quiet<->active boundary after dt_eastern: the next 9 AM if
    currently quiet, else the next 9 PM."""
    target = QUIET_END if _is_quiet_eastern(dt_eastern) else QUIET_START
    candidate = dt_eastern.replace(hour=target.hour, minute=0, second=0, microsecond=0)
    if candidate <= dt_eastern:
        candidate += timedelta(days=1)
    return candidate


def add_active_duration(start: datetime, seconds: float) -> datetime:
    """Returns `start` advanced by `seconds` of ACTIVE (non-quiet-hours)
    time, skipping every 9 PM-9 AM Eastern window encountered along the
    way. Accepts either an aware or naive-UTC `start`; always returns
    naive UTC, matching this app's usual datetime convention."""
    remaining = timedelta(seconds=seconds)
    current = _to_eastern(start)
    while remaining > timedelta(0):
        if _is_quiet_eastern(current):
            # No time counts while quiet -- jump straight to the next 9 AM.
            current = _next_transition(current)
            continue
        boundary = _next_transition(current)  # next 9 PM
        available = boundary - current
        if available >= remaining:
            current = current + remaining
            remaining = timedelta(0)
        else:
            remaining -= available
            current = boundary
    return _to_utc_naive(current)
