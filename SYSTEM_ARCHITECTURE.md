# Bro-Buddy System Architecture

## Overview

Bro-Buddy is designed as a **layered AI pipeline** where each module performs a dedicated function in order to ensure safety, routing accuracy, and controlled interaction with the LLM.

This architecture allows the system to remain **modular, observable, and maintainable**.

---

## Pipeline Architecture

```
config
   ↓
handler
   ↓
capacity_guard
   ↓
privacy_guard
   ↓
firewall
   ↓
routing
   ↓
memory
   ↓
orchestrator
   ↓
llm_client
   ↓
prompt
   ↓
validator
   ↓
logging_utils
```

---

## Layer Responsibilities

### Config

Stores global configuration values including model parameters and system constants.

### Handler

Acts as the AWS Lambda entry point and initializes the request processing pipeline.

### Capacity Guard

Protects the system from excessive request volume and prevents LLM cost spikes.

### Privacy Guard

Detects and masks personally identifiable information before it reaches the model.

### Firewall

Blocks prompt injection attacks and attempts to extract system architecture.

### Routing

Classifies user intent and determines whether the request requires LLM interaction.

### Memory

Maintains conversation history for session continuity.

### Orchestrator

Coordinates communication between routing decisions, prompts, and model execution.

### LLM Client

Handles interaction with the AWS Bedrock model.

### Prompt

Defines the system prompt and ensures consistent AI behavior.

### Validator

Validates model responses to prevent leakage of system instructions or infrastructure details.

### Logging Utilities

Records structured events for monitoring and debugging.

---

## Design Goals

The architecture prioritizes:

Safety
Preventing misuse and prompt injection.

Transparency
Providing clear observability of system behavior.

Modularity
Allowing individual components to evolve independently.

Cost Control
Reducing unnecessary LLM calls through deterministic routing.

---
