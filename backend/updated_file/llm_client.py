"""
llm_client.py
-------------
Handles Amazon Bedrock invocation for Claude models.

Responsibilities:
- Safe Bedrock invocation
- Structured logging
- Defensive response parsing
- Response size safety control
- Controlled failure behavior

No routing logic.
No business logic.
"""

import json
import time
import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from config import (
    ARN_INFERENCE,
    MAX_TOKENS,
    TEMPERATURE,
    BEDROCK_REGION,
    MAX_OUTPUT_WORDS
)

from logging_utils import log_event


# --------------------------------------------------
# Bedrock Runtime Client (With Timeout Safety)
# --------------------------------------------------

bedrock_runtime = boto3.client(
    "bedrock-runtime",
    region_name=BEDROCK_REGION,
    config=Config(
        read_timeout=25,
        connect_timeout=10,
        retries={"max_attempts": 2}
    )
)


# --------------------------------------------------
# Public LLM Invocation
# --------------------------------------------------

def call_llm(system_prompt: str, messages: list, request_id: str) -> str:
    """
    Sends prompt to Bedrock Claude and returns generated text.

    This function must never raise raw AWS errors.
    It must fail gracefully.
    """

    start_time = time.time()

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "system": system_prompt,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
        "messages": messages
    }

    try:

        log_event(
            "llm_request_started",
            request_id=request_id,
            model_id=ARN_INFERENCE
        )

        response = bedrock_runtime.invoke_model(
            modelId=ARN_INFERENCE,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )

        latency_ms = int((time.time() - start_time) * 1000)

        response_body = json.loads(response["body"].read())

        # --------------------------------------------------
        # Defensive Response Parsing
        # --------------------------------------------------

        content = response_body.get("content", [])

        if not content:

            log_event(
                "llm_response_invalid",
                request_id=request_id,
                model_id=ARN_INFERENCE
            )

            return _safe_failure_response()

        text_parts = []

        for block in content:
            if isinstance(block, dict) and "text" in block:
                text_parts.append(block["text"])

        if not text_parts:

            log_event(
                "llm_response_missing_text",
                request_id=request_id,
                model_id=ARN_INFERENCE
            )

            return _safe_failure_response()

        output_text = " ".join(text_parts).strip()

        if not output_text:

            log_event(
                "llm_empty_response",
                request_id=request_id,
                model_id=ARN_INFERENCE
            )

            return _safe_failure_response()

        # --------------------------------------------------
        # Response Size Safety Control
        # --------------------------------------------------

        words = output_text.split()

        if len(words) > MAX_OUTPUT_WORDS:
            output_text = " ".join(words[:MAX_OUTPUT_WORDS])

        log_event(
            "llm_request_completed",
            request_id=request_id,
            model_id=ARN_INFERENCE,
            latency_ms=latency_ms,
            response_words=len(output_text.split()),
            response_chars=len(output_text)
        )

        return output_text


    except (BotoCoreError, ClientError) as aws_error:

        log_event(
            "llm_aws_error",
            request_id=request_id,
            model_id=ARN_INFERENCE,
            error=str(aws_error)
        )

        return _safe_failure_response()


    except Exception as e:

        log_event(
            "llm_unknown_error",
            request_id=request_id,
            model_id=ARN_INFERENCE,
            error=str(e)
        )

        return _safe_failure_response()


# --------------------------------------------------
# Safe Failure Response
# --------------------------------------------------

def _safe_failure_response() -> str:
    """
    Returns a safe fallback message.
    Never expose internal errors to user.
    """

    return (
        "I’m having trouble generating a response right now. "
        "Please try again in a moment."
    )