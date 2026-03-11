# Bro-Buddy — Governance-First AI Companion System

## Overview

Bro-Buddy is a **production-style AI companion system** designed with safety, governance, and modular architecture in mind.

Unlike simple chatbot implementations, Bro-Buddy introduces a **layered AI pipeline** that includes guardrails, routing logic, prompt governance, and response validation to ensure responsible AI behavior.

The system demonstrates how modern AI assistants can be built with **enterprise-level safety and observability principles**.

---

## Key Features

• Deterministic routing for greetings and simple queries
• Dual operating modes (Professional Mode and AI Mode)
• Prompt firewall to prevent prompt injection and architecture probing
• Privacy guard that detects and masks personally identifiable information (PII)
• Capacity guard to prevent excessive LLM usage and control costs
• Conversational memory for session continuity
• Response validation to prevent prompt leakage and unsafe outputs
• Structured logging for full pipeline observability

---

## System Pipeline

The backend follows a **layered AI pipeline architecture**:

```
config → handler → capacity_guard → privacy_guard → firewall → routing → memory → orchestrator → llm_client → prompt → validator → logging_utils
```

Each component performs a specific function to ensure **safety, reliability, and maintainability**.

---

## Technology Stack

Frontend
• HTML
• CSS

Backend
• Python

AI Model
• AWS Bedrock (Claude)

Infrastructure
• AWS Lambda
• API Gateway
• CloudWatch Logs

---

## Project Structure

```
bro-buddy/

frontend/
   index.html
   style.css
   README.md

backend/
   handler.py
   routing.py
   orchestrator.py
   llm_client.py
   firewall.py
   privacy_guard.py
   capacity_guard.py
   validator.py
   memory_store.py
   logging_utils.py
   README.md

docs/
   SYSTEM_ARCHITECTURE.md
   SYSTEM_WORKFLOW.md

evaluation/

README.md
```

---

## Architecture Philosophy

The project was designed around the following principles:

Safety First
Multiple guardrails protect the system from misuse and prompt injection.

Deterministic Routing
Simple queries are handled without calling the LLM to reduce cost and latency.

Observability
Every stage of the pipeline generates structured logs for monitoring and debugging.

Modular Design
Each module performs a clearly defined responsibility.

---

## Deployment

The system is deployed using a **serverless architecture**.

```
User Interface
     ↓
API Gateway
     ↓
AWS Lambda
     ↓
AWS Bedrock LLM
     ↓
CloudWatch Logging
```

This architecture enables scalability while minimizing infrastructure overhead.

---

## Future Improvements

Planned improvements include:

• enhanced intent classification
• safety keyword routing for medical queries
• improved conversational memory management
• advanced evaluation metrics
• response quality benchmarking

---

## Project Goal

The goal of this project is to demonstrate how a **governance-first AI system** can be designed, evaluated, and deployed using production-style architecture.

This repository focuses on **system design, safety engineering, and AI pipeline governance** rather than building a simple chatbot interface.
