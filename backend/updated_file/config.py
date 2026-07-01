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

# Empty / whitespace guard (does not change behavior)
if not ARN_INFERENCE or not ARN_INFERENCE.strip():
    raise RuntimeError(
        "ARN_INFERENCE environment variable is not set. "
        "Lambda cannot start without a Bedrock inference profile ARN."
    )

# sanitize (safe, no logic change)
ARN_INFERENCE = ARN_INFERENCE.strip()


# ==========================================================
# Governance Validation
# ==========================================================

INFERENCE_PROFILE_PATTERN = (
    r"^arn:aws:bedrock:"
    r"([a-z0-9-]+):"   # capture region (non-breaking change)
    r"\d{12}:"
    r"inference-profile/"
    r"[A-Za-z0-9._:-]+$"
)

match = re.match(INFERENCE_PROFILE_PATTERN, ARN_INFERENCE)

if not match:
    raise RuntimeError(
        "Invalid ARN_INFERENCE. Must be a valid Bedrock inference profile ARN."
    )

# extract region (no impact unless used)
ARN_REGION = match.group(1)


# ==========================================================
# Environment Configuration
# ==========================================================

ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev").strip().lower()

BEDROCK_REGION = os.environ.get("BEDROCK_REGION", "us-east-1")

# empty guard (safe)
if not BEDROCK_REGION or not BEDROCK_REGION.strip():
    raise RuntimeError("BEDROCK_REGION cannot be empty")

BEDROCK_REGION = BEDROCK_REGION.strip()

# ==========================================================
# Region Consistency Check (NON-BREAKING SAFETY)
# ==========================================================

# prevents runtime Bedrock failure
if ARN_REGION != BEDROCK_REGION:
    raise RuntimeError(
        f"Region mismatch: ARN region ({ARN_REGION}) != BEDROCK_REGION ({BEDROCK_REGION})"
    )
# ==========================================================
# Model Metadata
# ==========================================================

MODEL_NAME = "claude"
PROMPT_VERSION = "v1.0"


# ==========================================================
# LLM Generation Parameters (Cost-Controlled Defaults)
# ==========================================================

MAX_TOKENS = 360
TEMPERATURE = 0.3


# ==========================================================
# System Limits
# ==========================================================

MAX_INPUT_LENGTH = 2000
MAX_OUTPUT_WORDS = 350
MAX_OUTPUT_PARAGRAPHS = 10

DEFAULT_MODE = "professional"


# ==========================================================
# Mode Configuration (Future-proof)
# ==========================================================

ALLOWED_MODES = {"professional", "ai"}
ENABLE_MODE_GUARD = True


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

MAX_ACTIVE_SESSIONS = 100


# ==========================================================
# Intent Constants (Clean + Reusable)
# ==========================================================

INTENT_GREETING = "greeting"
INTENT_SYSTEM = "system_explanation"
INTENT_AI = "ai_knowledge"
INTENT_PROFESSIONAL = "professional_reasoning"
INTENT_VAGUE = "vague"


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

IDENTITY_PATTERNS_SIMPLE = [
    "who are you",
    "what are you",
    "about you",
    "tell me about yourself"
]


# ==========================================================
# Retrieval Configuration (Future RAG)
# ==========================================================

ENABLE_RAG = False

TOP_K_RETRIEVAL = 3

SIMILARITY_HIGH = 0.80
SIMILARITY_MEDIUM = 0.60
SIMILARITY_LOW = 0.0


# ==========================================================
# Observability & Logging
# ==========================================================

ENABLE_STRUCTURED_LOGGING = True
LOG_TRUNCATED_QUERY_LENGTH = 120