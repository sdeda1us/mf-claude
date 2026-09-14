"""Shared auction timing constants.

Split out from auction_timer.py so auction_service.py -- which
auction_timer.py itself already imports from -- can use them too (e.g. to
compute the nomination deadline for display) without a circular import.
"""

NOMINATION_TIMEOUT_SECONDS = 3 * 60 * 60  # 3 hours

# A freshly-opened item's bid window is BID_TIMEOUT_SECONDS (3 hours)
# normally, or BID_TIMEOUT_EXTENDED_SECONDS (8 hours) instead whenever that
# base 3-hour window would touch the 9 PM-9 AM Eastern quiet hours at all --
# starts inside it, or runs long enough to reach it before the 3 hours are
# up (see quiet_hours.bid_window_deadline, which decides between the two
# and applies the usual quiet-hours skip on top either way).
BID_TIMEOUT_SECONDS = 3 * 60 * 60  # 3 hours
BID_TIMEOUT_EXTENDED_SECONDS = 8 * 60 * 60  # 8 hours

BID_EXTENSION_THRESHOLD_SECONDS = 10 * 60  # 10 minutes
BID_EXTENSION_SECONDS = 10 * 60  # 10 minutes
