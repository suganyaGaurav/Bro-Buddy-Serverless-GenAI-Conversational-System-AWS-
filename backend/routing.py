"""
routing.py
----------
Deterministic intent routing for Bro-Buddy.

Responsibilities:
- Greeting detection
- AI contextual detection
- Personal context detection
- Vague fallback detection
- Mode authority fallback

This module:
- Does NOT log
- Does NOT call LLM
- Does NOT access firewall
- Returns intent only
"""

import re
from config import (
    VAGUE_WORD_THRESHOLD,
    VAGUE_KEYWORDS,
    GREETING_PATTERNS,
    PERSONAL_CONTEXT_PATTERNS,
    AI_CONTEXT_PAIRS,
    AI_KEYWORDS
)


# ==================================================
# Public Classification Entry
# ==================================================

def classify_intent(user_query: str, mode: str) -> str:
    """
    Returns one of:
    - greeting
    - vague
    - professional_reasoning
    - ai_knowledge
    """

    text = (user_query or "").lower().strip()
    words = text.split()

    # Precompute expensive checks once
    ai_keyword_flag = _has_ai_keyword(text)
    ai_pair_flag = _has_ai_context_pair(text)

    # 1️⃣ Greeting (Highest Priority)
    if _is_greeting(text):
        return "greeting"

    # 2️⃣ AI Context Pair (Strongest Signal)
    if ai_pair_flag:
        return "ai_knowledge"

    # 3️⃣ AI Keyword Detection
    if ai_keyword_flag:
        return "ai_knowledge"

    # 4️⃣ Personal Context
    if _has_personal_context(text):
        return "professional_reasoning"

    # 5️⃣ Vague Detection
    if _is_vague(text, words, ai_keyword_flag):
        return "vague"

    # 6️⃣ Mode Authority Fallback
    if mode == "ai":
        return "ai_knowledge"

    # 7️⃣ Default
    return "professional_reasoning"


# ==================================================
# Detection Helpers
# ==================================================

def _is_greeting(text: str) -> bool:
    for pattern in GREETING_PATTERNS:
        if re.match(pattern, text):
            return True
    return False


def _is_vague(text: str, words: list, ai_keyword_flag: bool) -> bool:
    """
    Vague detection is strict fallback logic.
    AI keywords must NEVER be classified as vague.
    """

    if ai_keyword_flag:
        return False

    # Very short queries
    if len(words) <= VAGUE_WORD_THRESHOLD:
        return True

    # Keyword-based vague detection
    for keyword in VAGUE_KEYWORDS:
        if re.search(rf"\b{re.escape(keyword)}\b", text):
            return True

    return False


def _has_personal_context(text: str) -> bool:
    for pattern in PERSONAL_CONTEXT_PATTERNS:
        if re.search(pattern, text):
            return True
    return False


def _has_ai_context_pair(text: str) -> bool:
    for word1, word2 in AI_CONTEXT_PAIRS:
        if (
            re.search(rf"\b{re.escape(word1)}\b", text)
            and re.search(rf"\b{re.escape(word2)}\b", text)
        ):
            return True
    return False


def _has_ai_keyword(text: str) -> bool:
    for keyword in AI_KEYWORDS:
        if re.search(rf"\b{re.escape(keyword)}\b", text):
            return True
    return False