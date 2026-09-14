"""Shared auction timing constants.

Split out from auction_timer.py so auction_service.py -- which
auction_timer.py itself already imports from -- can use them too (e.g. to
compute the nomination deadline for display) without a circular import.
"""

NOMINATION_TIMEOUT_SECONDS = 3 * 60 * 60  # 3 hours
BID_TIMEOUT_SECONDS = 8 * 60 * 60  # 8 hours
BID_EXTENSION_THRESHOLD_SECONDS = 10 * 60  # 10 minutes
BID_EXTENSION_SECONDS = 10 * 60  # 10 minutes
