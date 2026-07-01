"""
handler.py
----------
AWS Lambda entry point.

Responsibilities:
- Parse and validate request
- Run capacity guard
- Run privacy guard
- Run firewall
- Call orchestrator
- Handle errors safely
- Return structured response

Business logic is NOT handled here.
"""

import json
import time

from orchestrator import process_chat
from capacity_guard import check_daily_capacity, release_request
from firewall import firewall_scan
from privacy_guard import mask_pii
from logging_utils import log_event
from config import (
    MAX_INPUT_LENGTH,
    DEFAULT_MODE,
    LOG_TRUNCATED_QUERY_LENGTH
)

# Minimum query size to prevent meaningless inputs
MIN_QUERY_LENGTH = 2


def lambda_handler(event, context):

    request_id = context.aws_request_id

    # --------------------------------------------------
    # Handle CORS Preflight
    # --------------------------------------------------

    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": _cors_headers(),
            "body": ""
        }

    log_event("request_received", request_id=request_id)

    user_query = ""
    mode = DEFAULT_MODE
    session_id = request_id  # default session fallback

    # --------------------------------------------------
    # Parse API Gateway body
    # --------------------------------------------------

    try:

        if "body" in event and event["body"]:

            body = json.loads(event["body"])

            user_query = body.get("query", "")
            mode = body.get("mode", DEFAULT_MODE)

            # --------------------------------------------------
            # Session ID for conversational memory
            # --------------------------------------------------

            session_id = body.get("session_id", request_id)

    except Exception as e:

        log_event(
            "request_parsing_failed",
            request_id=request_id,
            error=str(e)
        )

        return _error_response("Invalid request format.")

    # --------------------------------------------------
    # Normalize Mode
    # --------------------------------------------------

    mode = (mode or DEFAULT_MODE).strip().lower()

    if mode != "ai":
        mode = DEFAULT_MODE

    # --------------------------------------------------
    # Basic Input Validation
    # --------------------------------------------------

    user_query = (user_query or "").strip()

    if not user_query:
        return _error_response("Query cannot be empty.", status_code=400)

    if len(user_query) < MIN_QUERY_LENGTH:
        return _error_response("Query too short.", status_code=400)

    if len(user_query) > MAX_INPUT_LENGTH:
        return _error_response("Query exceeds allowed length.", status_code=400)

    log_event(
        "request_validated",
        request_id=request_id,
        mode=mode,
        input_length=len(user_query),
        query_preview=user_query[:LOG_TRUNCATED_QUERY_LENGTH]
    )

    # --------------------------------------------------
    # 1️⃣ Capacity Guard
    # --------------------------------------------------

    capacity_result = check_daily_capacity(request_id)

    log_event(
        "capacity_checked",
        request_id=request_id,
        over_limit=capacity_result["over_limit"]
    )

    if capacity_result["over_limit"]:

        return {
            "statusCode": 200,
            "headers": _cors_headers(),
            "body": json.dumps({
                "answer": capacity_result["response"],
                "mode": mode,
                "request_id": request_id
            })
        }

    try:

        # --------------------------------------------------
        # 2️⃣ Privacy Guard
        # --------------------------------------------------

        user_query = mask_pii(user_query, request_id)

        # --------------------------------------------------
        # 3️⃣ Firewall Scan
        # --------------------------------------------------

        firewall_result = firewall_scan(user_query, request_id)

        log_event(
            "firewall_checked",
            request_id=request_id,
            blocked=firewall_result["blocked"],
            category=firewall_result.get("reason_category"),
            severity=firewall_result.get("severity")
        )

        if firewall_result["blocked"]:

            return {
                "statusCode": 200,
                "headers": _cors_headers(),
                "body": json.dumps({
                    "answer": firewall_result["response"],
                    "mode": mode,
                    "request_id": request_id
                })
            }

        # --------------------------------------------------
        # 4️⃣ Orchestrator Execution
        # --------------------------------------------------

        start_time = time.time()

        answer = process_chat(
            user_query=user_query,
            mode=mode,
            request_id=request_id,
            session_id=session_id
        )

        latency_ms = int((time.time() - start_time) * 1000)

        log_event(
            "chat_processed",
            request_id=request_id,
            latency_ms=latency_ms
        )

        return {
            "statusCode": 200,
            "headers": _cors_headers(),
            "body": json.dumps({
                "answer": answer,
                "mode": mode,
                "request_id": request_id
            })
        }

    except Exception as e:

        log_event(
            "chat_processing_failed",
            request_id=request_id,
            error=str(e)
        )

        return _error_response("Chat processing failed.")

    finally:

        release_request(request_id)


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def _error_response(message, status_code=500):

    return {
        "statusCode": status_code,
        "headers": _cors_headers(),
        "body": json.dumps({
            "status": "error",
            "message": message
        })
    }


def _cors_headers():

    return {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST,OPTIONS"
    }