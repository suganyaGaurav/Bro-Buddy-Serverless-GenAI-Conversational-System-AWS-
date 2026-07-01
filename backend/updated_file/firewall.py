"""
firewall.py
-----------
Deterministic request firewall for Bro-Buddy.

Responsibilities:
- Accept raw user query
- Detect unsafe, injection, identity probing, prompt extraction
- Return structured decision metadata
- Never call LLM
- Never access mode
- Never perform routing
"""

import re
from typing import Dict, Optional


# ==========================================================
# 🔒 Deterministic Response Constants
# ==========================================================

UNSAFE_RESPONSE = (
    "I’m not able to provide that kind of advice. "
    "It would be best to consult a qualified professional."
)

INJECTION_RESPONSE = (
    "I’m not able to modify my operational boundaries."
)

IDENTITY_RESPONSE = (
    "I am Bro-Buddy, a serverless AI companion designed for grounded conversation."
)


# ==========================================================
# 🧱 Keyword Buckets (Exact Match Layer)
# ==========================================================

UNSAFE_KEYWORDS = [
    "medical advice",
    "dosage",
    "prescription",
    "legal advice",
    "sue someone",
    "self harm",
    "suicide",
    "depression treatment"
]


MEDICAL_SYMPTOM_KEYWORDS = [
    "chest pain",
    "headache",
    "fever",
    "shortness of breath",
    "blood pressure",
    "heart attack",
    "stroke",
    "dizziness",
    "nausea",
    "infection",
    "injury",
    "symptoms"
]


MEDICAL_ADVISORY_PATTERNS = [
    r"what should i do",
    r"how do i treat",
    r"is this serious",
    r"should i see",
    r"do i need",
    r"i have .*",
    r"i’ve been .*",
    r"i am experiencing .*"
]


INJECTION_KEYWORDS = [
    "ignore previous instructions",
    "override system",
    "reveal hidden instructions",
    "act as developer",
    "bypass safety",
    "jailbreak"
]


IDENTITY_KEYWORDS = [
    "who built you",
    "who created you",
    "what model are you",
    "are you claude",
    "are you openai",
    "system prompt",
    "which model powers you",
    "which company built you",
    "who trained you"
]


# ==========================================================
# 🔍 Regex Pattern Buckets (Flexible Match Layer)
# ==========================================================

UNSAFE_PATTERNS = [
    r"how much .* mg",
    r"what medication .*",
    r"diagnose .*",
]


INJECTION_PATTERNS = [
    r"ignore .* instructions",
    r"reveal .* prompt",
    r"bypass .* safety",
    r"override .* system",
]


IDENTITY_PATTERNS = [
    r"who .* (built|created|made|trained) you",
    r"what .* model .* you",
    r"where .* run",
]


PROMPT_EXTRACTION_PATTERNS = [
    r"hidden instructions",
    r"instruction prompt",
    r"internal instructions",
    r"instructions that guide your responses",
    r"prompt used to configure",
    r"prompt used to initialize",
    r"system initialization prompt",
    r"assistant system prompt",
    r"alignment instructions",
    r"developers expose system prompts"
]


ARCHITECTURE_PATTERNS = [
    r"assistant architecture",
    r"backend architecture",
    r"system architecture",
    r"model provider",
    r"system design behind",
    r"how .* backend",
    r"how .* architecture",
    r"how .* system works",
    r"what infrastructure",
]


# ==========================================================
# 🛡 Detection Helpers
# ==========================================================

def _match_keywords(query: str, keywords: list) -> bool:
    for keyword in keywords:
        if re.search(rf"\b{re.escape(keyword)}\b", query, re.IGNORECASE):
            return True
    return False


def _match_patterns(query: str, patterns: list) -> bool:
    return any(re.search(pattern, query, re.IGNORECASE) for pattern in patterns)


# ==========================================================
# 🔥 Category Detection Functions
# ==========================================================

def _detect_medical_context(query: str) -> Optional[Dict]:

    symptom_match = any(symptom in query for symptom in MEDICAL_SYMPTOM_KEYWORDS)
    advisory_match = _match_patterns(query, MEDICAL_ADVISORY_PATTERNS)

    if symptom_match and advisory_match:
        return {
            "reason_category": "restricted_medical",
            "reason_detail": "symptom_context_match",
            "severity": "high",
            "response": UNSAFE_RESPONSE
        }

    return None


def _detect_unsafe(query: str) -> Optional[Dict]:

    if _match_keywords(query, UNSAFE_KEYWORDS):
        return {
            "reason_category": "unsafe",
            "reason_detail": "keyword_match",
            "severity": "high",
            "response": UNSAFE_RESPONSE
        }

    if _match_patterns(query, UNSAFE_PATTERNS):
        return {
            "reason_category": "unsafe",
            "reason_detail": "regex_match",
            "severity": "high",
            "response": UNSAFE_RESPONSE
        }

    medical_context = _detect_medical_context(query)
    if medical_context:
        return medical_context

    return None


def _detect_prompt_extraction(query: str) -> Optional[Dict]:

    if _match_patterns(query, PROMPT_EXTRACTION_PATTERNS):
        return {
            "reason_category": "prompt_extraction",
            "reason_detail": "semantic_pattern",
            "severity": "high",
            "response": INJECTION_RESPONSE
        }

    return None


def _detect_architecture_probe(query: str) -> Optional[Dict]:

    if _match_patterns(query, ARCHITECTURE_PATTERNS):
        return {
            "reason_category": "architecture_disclosure",
            "reason_detail": "semantic_pattern",
            "severity": "medium",
            "response": IDENTITY_RESPONSE
        }

    return None


def _detect_injection(query: str) -> Optional[Dict]:

    if _match_keywords(query, INJECTION_KEYWORDS):
        return {
            "reason_category": "injection",
            "reason_detail": "keyword_match",
            "severity": "high",
            "response": INJECTION_RESPONSE
        }

    if _match_patterns(query, INJECTION_PATTERNS):
        return {
            "reason_category": "injection",
            "reason_detail": "regex_match",
            "severity": "high",
            "response": INJECTION_RESPONSE
        }

    return None


def _detect_identity(query: str) -> Optional[Dict]:

    if _match_keywords(query, IDENTITY_KEYWORDS):
        return {
            "reason_category": "identity_probe",
            "reason_detail": "keyword_match",
            "severity": "medium",
            "response": IDENTITY_RESPONSE
        }

    if _match_patterns(query, IDENTITY_PATTERNS):
        return {
            "reason_category": "identity_probe",
            "reason_detail": "regex_match",
            "severity": "medium",
            "response": IDENTITY_RESPONSE
        }

    return None


# ==========================================================
# 🚪 Public Firewall Entry Point
# ==========================================================

def firewall_scan(query: str, request_id: str) -> Dict:

    normalized_query = (query or "").strip().lower()

    unsafe_result = _detect_unsafe(normalized_query)
    if unsafe_result:
        return {"blocked": True, **unsafe_result}

    prompt_result = _detect_prompt_extraction(normalized_query)
    if prompt_result:
        return {"blocked": True, **prompt_result}

    arch_result = _detect_architecture_probe(normalized_query)
    if arch_result:
        return {"blocked": True, **arch_result}

    injection_result = _detect_injection(normalized_query)
    if injection_result:
        return {"blocked": True, **injection_result}

    identity_result = _detect_identity(normalized_query)
    if identity_result:
        return {"blocked": True, **identity_result}

    return {
        "blocked": False,
        "reason_category": None,
        "reason_detail": None,
        "severity": None,
        "response": None
    }