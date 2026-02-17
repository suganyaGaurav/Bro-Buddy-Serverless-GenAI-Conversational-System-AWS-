"""
handler.py
----------
AWS Lambda entry point.
"""

import json
import logging

from prompt import build_prompt
from llm_client import call_llm

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    # Defaults
    user_query = "Say hello in one sentence."
    mode = "professional"

    # Parse API Gateway body
    try:
        if "body" in event and event["body"]:
            body = json.loads(event["body"])
            user_query = body.get("query", user_query)
            mode = body.get("mode", mode)
    except Exception as e:
        logger.error("Failed to parse request body: %s", str(e))

    logger.info("Query: %s | Mode: %s", user_query, mode)

    # Build Bedrock-compatible prompt
    system_prompt, messages = build_prompt(user_query, mode)

    # Call LLM
    answer = call_llm(system_prompt, messages)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "POST,OPTIONS"
        },
        "body": json.dumps({
            "answer": answer
        })
    }
