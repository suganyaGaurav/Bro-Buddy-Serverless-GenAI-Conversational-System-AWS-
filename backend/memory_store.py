"""
memory_store.py
---------------
Lightweight in-memory conversation memory for Bro-Buddy.

Responsibilities:
- Store short conversation history per session
- Limit memory window
- Provide safe retrieval
- Expire inactive sessions
- Emit observability logs

This is an MVP implementation.

Later this module can be replaced with:
- Redis
- DynamoDB
- Vector memory store
"""

import time

from config import MEMORY_WINDOW, SESSION_TTL_SECONDS, MAX_ACTIVE_SESSIONS
from logging_utils import log_event


# --------------------------------------------------
# In-Memory Session Store (Lambda Container Scoped)
# --------------------------------------------------

_session_store = {}


# --------------------------------------------------
# Utility: Remove Expired Sessions
# --------------------------------------------------

def _cleanup_expired_sessions():

    now = time.time()

    expired_sessions = [
        sid for sid, data in _session_store.items()
        if now - data["last_updated"] > SESSION_TTL_SECONDS
    ]

    for sid in expired_sessions:
        del _session_store[sid]


# --------------------------------------------------
# Utility: Basic Injection Sanitization
# --------------------------------------------------

def _sanitize_message(message: str):

    blocked_patterns = [
        "ignore previous instructions",
        "reveal system prompt",
        "show system prompt",
        "developer mode",
        "print configuration"
    ]

    msg = message.lower()

    for pattern in blocked_patterns:
        if pattern in msg:
            return "[filtered-content]"

    return message


# --------------------------------------------------
# Fetch Conversation History
# --------------------------------------------------

def fetch_history(session_id: str, request_id: str):

    _cleanup_expired_sessions()

    session = _session_store.get(session_id)

    if not session:
        return []

    history = session["messages"]

    log_event(
        "memory_fetched",
        request_id=request_id,
        session_id=session_id,
        history_length=len(history)
    )

    # Return safe copy to avoid mutation outside module
    return history.copy()


# --------------------------------------------------
# Update Conversation History
# --------------------------------------------------

def update_history(session_id: str, user_query: str, assistant_reply: str, request_id: str):

    _cleanup_expired_sessions()

    # Session limit protection
    if len(_session_store) >= MAX_ACTIVE_SESSIONS:

        oldest_session = min(
            _session_store.items(),
            key=lambda item: item[1]["last_updated"]
        )[0]

        del _session_store[oldest_session]

        log_event(
            "memory_evicted_old_session",
            request_id=request_id,
            session_id=oldest_session
        )

    if session_id not in _session_store:

        _session_store[session_id] = {
            "messages": [],
            "last_updated": time.time()
        }

    session = _session_store[session_id]

    safe_user_query = _sanitize_message(user_query)
    safe_reply = _sanitize_message(assistant_reply)

    session["messages"].append({
        "role": "user",
        "content": safe_user_query
    })

    session["messages"].append({
        "role": "assistant",
        "content": safe_reply
    })

    # Keep only last N messages
    session["messages"] = session["messages"][-MEMORY_WINDOW:]

    session["last_updated"] = time.time()

    log_event(
        "memory_updated",
        request_id=request_id,
        session_id=session_id,
        history_length=len(session["messages"])
    )