"""
orchestrator.py
---------------
Central execution layer for Bro-Buddy.

Responsibilities:
- Receive classified intent
- Apply deterministic shortcuts
- Enforce mode governance
- Invoke LLM when required
- Validate model output
- Manage conversational memory
- Emit structured observability logs
"""

import time

from routing import classify_intent
from prompt import build_prompt
from llm_client import call_llm
from validator import validate_response
from logging_utils import log_event
from memory_store import fetch_history, update_history


# ==================================================
# Public Entry Point
# ==================================================

def process_chat(user_query: str, mode: str, request_id: str, session_id: str) -> str:

    start_time = time.time()

    # --------------------------------------------------
    # 1️⃣ Intent Classification
    # --------------------------------------------------

    intent = classify_intent(user_query, mode)

    log_event(
        "intent_classified",
        request_id=request_id,
        intent=intent,
        mode=mode
    )

    # --------------------------------------------------
    # 2️⃣ Deterministic Shortcuts
    # --------------------------------------------------

    if intent == "greeting":

        log_event(
            "routing_decision",
            request_id=request_id,
            route="deterministic",
            reason="greeting_shortcut"
        )

        response = _greeting_response(mode)

        # Store greeting in memory
        update_history(
            session_id=session_id,
            user_query=user_query,
            assistant_reply=response,
            request_id=request_id
        )

        return response

    if intent == "vague":

        log_event(
            "routing_decision",
            request_id=request_id,
            route="deterministic",
            reason="vague_input"
        )

        response = _clarification_response()

        # Store clarification interaction
        update_history(
            session_id=session_id,
            user_query=user_query,
            assistant_reply=response,
            request_id=request_id
        )

        return response

    # --------------------------------------------------
    # 3️⃣ Mode Authority Guard
    # --------------------------------------------------

    if intent == "professional_reasoning" and mode == "ai":

        log_event(
            "routing_decision",
            request_id=request_id,
            route="deterministic",
            reason="mode_mismatch_professional"
        )

        response = (
            "This appears to be a career or mentoring question. "
            "You may want to switch to Professional Mode for structured guidance."
        )

        update_history(
            session_id=session_id,
            user_query=user_query,
            assistant_reply=response,
            request_id=request_id
        )

        return response

    if intent == "ai_knowledge" and mode == "professional":

        log_event(
            "routing_decision",
            request_id=request_id,
            route="deterministic",
            reason="mode_mismatch_ai"
        )

        response = (
            "This appears to be a technical AI question. "
            "You can switch to AI Mode for deeper architectural explanations."
        )

        update_history(
            session_id=session_id,
            user_query=user_query,
            assistant_reply=response,
            request_id=request_id
        )

        return response

    # --------------------------------------------------
    # 4️⃣ LLM Invocation
    # --------------------------------------------------

    if intent in ("professional_reasoning", "ai_knowledge"):

        log_event(
            "routing_decision",
            request_id=request_id,
            route="llm",
            intent=intent,
            mode=mode
        )

        llm_start = time.time()

        # --------------------------------------------------
        # Fetch Conversation History (Memory)
        # --------------------------------------------------

        try:
            history = fetch_history(session_id, request_id)
        except Exception:

            log_event(
                "memory_fetch_failed",
                request_id=request_id
            )

            history = []

        # --------------------------------------------------
        # Build Prompt with Memory
        # --------------------------------------------------

        system_prompt, messages = build_prompt(
            user_query,
            history,
            mode
        )

        # --------------------------------------------------
        # Call LLM
        # --------------------------------------------------

        model_answer = call_llm(system_prompt, messages, request_id)

        llm_latency_ms = int((time.time() - llm_start) * 1000)

        # --------------------------------------------------
        # Validate Response
        # --------------------------------------------------

        validated_answer = validate_response(
            user_query=user_query,
            mode=mode,
            model_answer=model_answer,
            request_id=request_id,
            intent=intent
        )

        # --------------------------------------------------
        # Update Memory
        # --------------------------------------------------

        update_history(
            session_id=session_id,
            user_query=user_query,
            assistant_reply=validated_answer,
            request_id=request_id
        )

        total_latency_ms = int((time.time() - start_time) * 1000)

        output_word_estimate = len(validated_answer.split())

        log_event(
            "llm_completed",
            request_id=request_id,
            intent=intent,
            mode=mode,
            llm_latency_ms=llm_latency_ms,
            total_latency_ms=total_latency_ms,
            output_word_estimate=output_word_estimate
        )

        return validated_answer

    # --------------------------------------------------
    # 5️⃣ Safe Default
    # --------------------------------------------------

    log_event(
        "routing_decision",
        request_id=request_id,
        route="deterministic",
        reason="fallback_default"
    )

    response = _clarification_response()

    update_history(
        session_id=session_id,
        user_query=user_query,
        assistant_reply=response,
        request_id=request_id
    )

    return response


# ==================================================
# Deterministic Responses
# ==================================================

def _greeting_response(mode: str):

    if mode == "professional":
        return "Hello. What are you working through today?"
    else:
        return "Hey. What’s on your mind?"


def _clarification_response():

    return (
        "Could you share a bit more context so I can understand what you're looking for?"
    )