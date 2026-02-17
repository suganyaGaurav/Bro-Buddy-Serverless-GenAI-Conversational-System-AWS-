"""
llm_client.py
-------------
Handles Amazon Bedrock invocation for Claude models.
"""

import json
import boto3
import logging

from config import MODEL_ID, MAX_TOKENS, TEMPERATURE

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize Bedrock runtime client once (best practice)
bedrock_runtime = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1"  # must match your Bedrock region
)


def call_llm(system_prompt: str, messages: list) -> str:
    """
    Sends prompt to Bedrock Claude and returns generated text.
    """

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "system": system_prompt,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
        "messages": messages
    }

    response = bedrock_runtime.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(response["body"].read())
    return response_body["content"][0]["text"]
