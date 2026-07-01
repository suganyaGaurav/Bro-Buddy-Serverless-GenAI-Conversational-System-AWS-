"""
privacy_guard.py
----------------
PII masking layer for Bro-Buddy.

Responsibilities:
- Detect simple PII patterns
- Mask PII before firewall and LLM
- Preserve original message structure
- Emit observability logs

No routing logic.
No LLM calls.
"""

import re
from logging_utils import log_event


# --------------------------------------------------
# Mask Tokens (Centralized)
# --------------------------------------------------

EMAIL_MASK = "[EMAIL]"
PHONE_MASK = "[PHONE]"
CARD_MASK = "[CARD]"
ID_MASK = "[ID]"


# --------------------------------------------------
# PII Regex Patterns (Precompiled)
# --------------------------------------------------

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    re.IGNORECASE
)

# Slightly stricter phone pattern to reduce false positives
PHONE_PATTERN = re.compile(
    r"\b[6-9]\d{9}\b"
)

CREDIT_CARD_PATTERN = re.compile(
    r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b"
)

AADHAAR_PATTERN = re.compile(
    r"\b\d{4}\s?\d{4}\s?\d{4}\b"
)


# --------------------------------------------------
# Public Privacy Guard
# --------------------------------------------------

def mask_pii(user_query: str, request_id: str) -> str:
    """
    Masks common PII patterns before processing.
    """

    masked = user_query
    pii_detected = []

    # --------------------------------------------------
    # Email
    # --------------------------------------------------

    if EMAIL_PATTERN.search(masked):
        masked = EMAIL_PATTERN.sub(EMAIL_MASK, masked)
        pii_detected.append("email")

    # --------------------------------------------------
    # Phone
    # --------------------------------------------------

    if PHONE_PATTERN.search(masked):
        masked = PHONE_PATTERN.sub(PHONE_MASK, masked)
        pii_detected.append("phone")

    # --------------------------------------------------
    # Credit Card
    # --------------------------------------------------

    if CREDIT_CARD_PATTERN.search(masked):
        masked = CREDIT_CARD_PATTERN.sub(CARD_MASK, masked)
        pii_detected.append("card")

    # --------------------------------------------------
    # Aadhaar (India)
    # --------------------------------------------------

    if AADHAAR_PATTERN.search(masked):
        masked = AADHAAR_PATTERN.sub(ID_MASK, masked)
        pii_detected.append("aadhaar")

    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    if pii_detected:

        log_event(
            "privacy_guard_masked",
            request_id=request_id,
            pii_types=",".join(sorted(set(pii_detected))),
            pii_count=len(pii_detected)
        )

    return masked