"""
config.py
---------
Central configuration for Bro-Buddy.

Responsibilities:
- Environment validation
- Bedrock inference profile enforcement
- Cost control defaults
- Routing thresholds
- Retrieval configuration (future RAG)
- Observability toggles

This file must contain constants only.
No business logic.
"""

import os
import re


# ==========================================================
# Required Environment Configuration
# ==========================================================

ARN_INFERENCE = os.environ.get("ARN_INFERENCE")

if not ARN_INFERENCE:
    raise RuntimeError(
        "ARN_INFERENCE environment variable is not set. "
        "Lambda cannot start without a Bedrock inference profile ARN."
    )


# ==========================================================
# Governance Validation
# ==========================================================

INFERENCE_PROFILE_PATTERN = (
    r"^arn:aws:bedrock:"
    r"[a-z0-9-]+:"
    r"\d{12}:"
    r"inference-profile/"
    r"[A-Za-z0-9._:-]+$"
)

if not re.match(INFERENCE_PROFILE_PATTERN, ARN_INFERENCE):
    raise RuntimeError(
        "Invalid ARN_INFERENCE. Must be a valid Bedrock inference profile ARN."
    )


# ==========================================================
# Environment Configuration
# ==========================================================

ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")
BEDROCK_REGION = os.environ.get("BEDROCK_REGION", "us-east-1")


# ==========================================================
# Model Metadata
# ==========================================================

MODEL_NAME = "claude"
PROMPT_VERSION = "v1.0"


# ==========================================================
# LLM Generation Parameters (Cost-Controlled Defaults)
# ==========================================================

MAX_TOKENS = 280
TEMPERATURE = 0.3


# ==========================================================
# System Limits
# ==========================================================

MAX_INPUT_LENGTH = 2000
MAX_OUTPUT_WORDS = 250
MAX_OUTPUT_PARAGRAPHS = 6

DEFAULT_MODE = "professional"


# ==========================================================
# Capacity Guard Limits
# ==========================================================

DAILY_REQUEST_LIMIT = 500
ACTIVE_REQUEST_LIMIT = 30


# ==========================================================
# Memory Configuration (Conversational Memory)
# ==========================================================

MEMORY_WINDOW = 6
SESSION_TTL_SECONDS = 900

# Maximum active sessions allowed in Lambda container
MAX_ACTIVE_SESSIONS = 100


# ==========================================================
# Intent Routing Configuration
# ==========================================================

VAGUE_WORD_THRESHOLD = 2

VAGUE_KEYWORDS = [
    "ok",
    "okay",
    "hmm",
    "yeah",
    "yep",
    "idk",
    "not sure",
    "maybe"
]

GREETING_PATTERNS = [
    r"^hi\b",
    r"^hello\b",
    r"^hey\b",
    r"^good morning\b",
    r"^good evening\b",
    r"^good afternoon\b"
]

PERSONAL_CONTEXT_PATTERNS = [
    r"\bmy work\b",
    r"\bmy project\b",
    r"\bmy resume\b",
    r"\bmy performance\b",
    r"\bmy career\b",
    r"\bmy job\b",
    r"\bmy code\b",
    r"\bmy plan\b"
]

AI_CONTEXT_PAIRS = [
    ("evaluation", "model"),
    ("evaluation", "metrics"),
    ("metrics", "machine learning"),
    ("llm", "evaluation"),
    ("rag", "evaluation"),
    ("transformer", "architecture")
]

AI_KEYWORDS = [
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "neural network",
    "transformer",
    "llm",
    "rag",
    "multi agent",
    "multi-agent",
    "mcp",
    "model context protocol",
    "embedding",
    "vector database",
    "inference",
    "fine tuning",
    "fine-tuning",
    "hallucination",
    "governance",
    "responsible ai",
    "ai security",
    "quantum computing"
]


# ==========================================================
# Retrieval Configuration (Future RAG)
# ==========================================================

TOP_K_RETRIEVAL = 3

SIMILARITY_HIGH = 0.80
SIMILARITY_MEDIUM = 0.60
SIMILARITY_LOW = 0.0


# ==========================================================
# Observability & Logging
# ==========================================================

ENABLE_STRUCTURED_LOGGING = True
LOG_TRUNCATED_QUERY_LENGTH = 120
