"""
prompt.py
---------
Prompt orchestration for Bro-Buddy.
Handles identity, tone, and mode behavior.
"""

def build_system_prompt(mode: str) -> str:
    """
    Builds the system prompt based on selected mode.
    """

    base_prompt = (
        "You are Bro-Buddy, a calm and grounded AI companion. "
        "You are not Claude, ChatGPT, or any other AI model. "
        "You support clear thinking, professional communication, "
        "and thoughtful everyday conversations. "
        "You do not provide medical, legal, or mental health advice."
    )

    if mode == "chill":
        mode_prompt = (
            "Use a relaxed, friendly, and supportive tone, "
            "while staying grounded and respectful."
        )
    else:
        # Default: professional
        mode_prompt = (
            "Use a professional, structured, and practical tone."
        )

    return f"{base_prompt}\n\n{mode_prompt}"


def build_prompt(user_query: str, mode: str):
    """
    Returns system prompt and messages separately
    (required by Anthropic Claude on Bedrock).
    """

    system_prompt = build_system_prompt(mode)

    messages = [
        {
            "role": "user",
            "content": user_query
        }
    ]

    return system_prompt, messages
