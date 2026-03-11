"""
validator.py
-------------
Response validation and safety enforcement layer for Bro-Buddy.

Responsibilities:
- Prevent prompt leakage
- Prevent infrastructure disclosure
- Remove formatting artifacts
- Enforce response size limits
- Provide safe fallback responses

This module does NOT perform routing or LLM calls.
"""

import re
from logging_utils import log_event
from config import MAX_OUTPUT_WORDS


# --------------------------------------------------
# Infrastructure Disclosure Keywords
# --------------------------------------------------

INFRA_KEYWORDS = [
    "aws",
    "bedrock",
    "claude",
    "anthropic",
    "inference profile",
    "modelid",
    "system prompt",
    "hidden instructions",
    "internal system"
]


# --------------------------------------------------
# System Identity Response
# --------------------------------------------------

IDENTITY_RESPONSE = (
    "I am Bro-Buddy, a serverless AI companion designed for grounded conversation."
)


# --------------------------------------------------
# Fallback Response
# --------------------------------------------------

def _fallback_general():

    return (
        "I’m having trouble generating a response right now. "
        "Please try again in a moment."
    )


# --------------------------------------------------
# Helper: Detect System Probe
# --------------------------------------------------

SYSTEM_PROBE_PATTERNS = [
    r"how (are|were) you built",
    r"what model (are|powers)",
    r"who created you",
    r"system prompt",
    r"hidden instructions",
    r"internal configuration",
]


def _is_system_probe(query: str):

    lowered = (query or "").lower()

    for pattern in SYSTEM_PROBE_PATTERNS:
        if re.search(pattern, lowered):
            return True

    return False


# --------------------------------------------------
# Public Validation Function
# --------------------------------------------------

def validate_response(
    user_query: str,
    mode: str,
    model_answer: str,
    request_id: str,
    intent: str = None
) -> str:

    modified = False

    # Normalize whitespace
    output = (model_answer or "").strip()
    output = re.sub(r"\s+\n", "\n", output)

    # --------------------------------------------------
    # 1️⃣ Empty Response Protection
    # --------------------------------------------------

    if not output:

        log_event(
            "validator_empty_output",
            request_id=request_id
        )

        return _fallback_general()

    # --------------------------------------------------
    # 2️⃣ Remove Markdown / Formatting
    # --------------------------------------------------

    if "```" in output:
        output = output.replace("```", "")
        modified = True

    output = re.sub(r"^#+\s*", "", output, flags=re.MULTILINE)
    output = re.sub(r"\*\*(.*?)\*\*", r"\1", output)
    output = re.sub(r"\*(.*?)\*", r"\1", output)

    lowered_output = output.lower()

    # --------------------------------------------------
    # 3️⃣ Prompt Echo Protection
    # --------------------------------------------------

    if "identity:" in lowered_output or "governance:" in lowered_output:

        log_event(
            "validator_prompt_echo_blocked",
            request_id=request_id,
            preview=output[:200]
        )

        return IDENTITY_RESPONSE

    # --------------------------------------------------
    # 4️⃣ Infrastructure Disclosure Protection
    # --------------------------------------------------

    if _is_system_probe(user_query):

        for keyword in INFRA_KEYWORDS:

            if re.search(rf"\b{re.escape(keyword)}\b", lowered_output):

                log_event(
                    "validator_infra_leak_blocked",
                    request_id=request_id,
                    keyword=keyword,
                    preview=output[:200]
                )

                return IDENTITY_RESPONSE

    # --------------------------------------------------
    # 5️⃣ Paragraph Limit
    # --------------------------------------------------

    paragraphs = [p.strip() for p in output.split("\n\n") if p.strip()]

    if len(paragraphs) > 6:

        output = "\n\n".join(paragraphs[:6])
        modified = True

    # --------------------------------------------------
    # 6️⃣ Word Limit
    # --------------------------------------------------

    words = output.split()

    if len(words) > MAX_OUTPUT_WORDS:

        output = " ".join(words[:MAX_OUTPUT_WORDS])
        modified = True

    # --------------------------------------------------
    # 7️⃣ Modification Logging
    # --------------------------------------------------

    if modified:

        log_event(
            "validator_modified_output",
            request_id=request_id
        )

    return output