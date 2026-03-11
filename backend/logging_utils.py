"""
logging_utils.py
----------------
Centralized structured logging for Bro-Buddy.

Purpose:
- Provide consistent enterprise log schema
- Enable observability across the pipeline
- Support debugging, monitoring, and auditing
- Ensure logs never break application execution

All logs are emitted as structured JSON.
"""

import logging
import json
import time
from datetime import datetime, timezone

from config import (
    MODEL_NAME,
    PROMPT_VERSION,
    ENVIRONMENT,
    LOG_TRUNCATED_QUERY_LENGTH
)


# --------------------------------------------------
# Logger Initialization
# --------------------------------------------------

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# --------------------------------------------------
# Utility: Safe Query Preview
# --------------------------------------------------

def _query_preview(text: str):

    if not text:
        return ""

    text = text.replace("\n", " ").strip()

    if len(text) > LOG_TRUNCATED_QUERY_LENGTH:
        return text[:LOG_TRUNCATED_QUERY_LENGTH] + "..."

    return text


# --------------------------------------------------
# Public Logging Interface
# --------------------------------------------------

def log_event(event_type: str, **kwargs):
    """
    Logs structured JSON events.

    Safe for production:
    - Never raises exceptions
    - Always produces consistent schema
    """

    epoch_time = int(time.time())

    payload = {

        # --------------------------------------------------
        # Core Event Metadata
        # --------------------------------------------------

        "event_type": event_type,
        "timestamp": epoch_time,
        "timestamp_iso": datetime.now(timezone.utc).isoformat(),

        # --------------------------------------------------
        # System Metadata
        # --------------------------------------------------

        "service": "bro-buddy",
        "environment": ENVIRONMENT,
        "model": MODEL_NAME,
        "prompt_version": PROMPT_VERSION
    }

    # --------------------------------------------------
    # Request ID Safety
    # --------------------------------------------------

    request_id = kwargs.pop("request_id", None)

    if request_id:
        payload["request_id"] = request_id
    else:
        payload["request_id"] = "missing_request_id"

    # --------------------------------------------------
    # Query Preview Protection
    # --------------------------------------------------

    if "query" in kwargs:
        payload["query_preview"] = _query_preview(kwargs.pop("query"))

    # --------------------------------------------------
    # Normalize Latency Fields
    # --------------------------------------------------

    if "latency_ms" in kwargs:
        try:
            kwargs["latency_ms"] = int(kwargs["latency_ms"])
        except Exception:
            kwargs["latency_ms"] = 0

    # --------------------------------------------------
    # Merge Remaining Fields
    # --------------------------------------------------

    payload.update(kwargs)

    # --------------------------------------------------
    # Safe Logging (Never Crash)
    # --------------------------------------------------

    try:

        logger.info(json.dumps(payload))

    except Exception:

        logger.info(json.dumps({

            "event_type": "logging_failure",
            "timestamp": int(time.time()),
            "timestamp_iso": datetime.now(timezone.utc).isoformat(),
            "service": "bro-buddy",
            "environment": ENVIRONMENT,
            "original_event_type": event_type

        }))