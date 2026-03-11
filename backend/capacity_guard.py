"""
capacity_guard.py
-----------------
Traffic protection layer for Bro-Buddy.

Responsibilities:
- Prevent excessive traffic
- Protect Bedrock usage costs
- Provide graceful rejection if limits exceeded
- Emit structured observability logs

Notes:
- Uses simple in-memory counters (Lambda container scoped)
- Suitable for MVP / portfolio deployment
- Can later be replaced by Redis or DynamoDB counters
"""

import time
from typing import Dict
from logging_utils import log_event
from config import DAILY_REQUEST_LIMIT, ACTIVE_REQUEST_LIMIT


# ==========================================================
# ⚙ Capacity Configuration (Centralized in config.py)
# ==========================================================

DAILY_LIMIT = DAILY_REQUEST_LIMIT
ACTIVE_LIMIT = ACTIVE_REQUEST_LIMIT


# ==========================================================
# ⚙ Internal Runtime State (Container Scoped)
# ==========================================================

_request_count = 0
_active_requests = 0
_last_reset_day = time.strftime("%Y-%m-%d")


# ==========================================================
# 🔄 Reset Daily Counter
# ==========================================================

def _reset_if_new_day():
    global _request_count
    global _last_reset_day

    current_day = time.strftime("%Y-%m-%d")

    if current_day != _last_reset_day:

        _request_count = 0
        _last_reset_day = current_day

        log_event(
            "capacity_daily_counter_reset",
            new_day=current_day
        )


# ==========================================================
# 🚪 Public Capacity Check
# ==========================================================

def check_daily_capacity(request_id: str) -> Dict:
    """
    Enforces request capacity limits.
    """

    global _request_count
    global _active_requests

    _reset_if_new_day()

    # --------------------------------------------------
    # Check Daily Limit
    # --------------------------------------------------

    if _request_count >= DAILY_LIMIT:

        log_event(
            "capacity_blocked_daily_limit",
            request_id=request_id,
            current_count=_request_count,
            daily_limit=DAILY_LIMIT
        )

        return {
            "over_limit": True,
            "current_count": _request_count,
            "daily_limit": DAILY_LIMIT,
            "response": (
                "Bro-Buddy is currently at daily capacity. "
                "Please try again later."
            )
        }

    # --------------------------------------------------
    # Check Concurrent Limit
    # --------------------------------------------------

    if _active_requests >= ACTIVE_LIMIT:

        log_event(
            "capacity_blocked_concurrent_limit",
            request_id=request_id,
            active_requests=_active_requests,
            active_limit=ACTIVE_LIMIT
        )

        return {
            "over_limit": True,
            "current_count": _request_count,
            "daily_limit": DAILY_LIMIT,
            "response": (
                "Bro-Buddy is currently handling many conversations. "
                "Please try again shortly."
            )
        }

    # --------------------------------------------------
    # Allow Request
    # --------------------------------------------------

    _request_count += 1
    _active_requests += 1

    log_event(
        "capacity_allowed",
        request_id=request_id,
        current_count=_request_count,
        active_requests=_active_requests
    )

    return {
        "over_limit": False,
        "current_count": _request_count,
        "daily_limit": DAILY_LIMIT,
        "response": None
    }


# ==========================================================
# 🔚 Release Active Request
# ==========================================================

def release_request(request_id: str):
    """
    Decrements active request counter after request completes.
    """

    global _active_requests

    # Prevent negative counter
    _active_requests = max(0, _active_requests - 1)

    log_event(
        "capacity_released",
        request_id=request_id,
        active_requests=_active_requests
    )