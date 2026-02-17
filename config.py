"""
config.py
---------
Central configuration for Bedrock LLM usage.
"""

import os

# Bedrock model ID (set as Lambda environment variable)
MODEL_ID = os.environ.get("MODEL_ID")

# LLM generation parameters
MAX_TOKENS = 150
TEMPERATURE = 0.3 # calm, grounded responses
