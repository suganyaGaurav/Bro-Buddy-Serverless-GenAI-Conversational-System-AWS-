# Bro-Buddy System Workflow

## Overview

This document describes the step-by-step flow of how a user request is processed within the Bro-Buddy system.

---

## Request Lifecycle

### Step 1 — User Input

The user enters a prompt in the frontend interface.

Example:

"How can I manage stress at work?"

The request is sent to the backend API.

---

### Step 2 — Request Handler

The Lambda handler receives the request and initializes the processing pipeline.

The request is validated to ensure it follows the expected format.

---

### Step 3 — Capacity Guard

The system checks whether current request traffic exceeds allowed limits.

If limits are exceeded, the request is rejected gracefully.

---

### Step 4 — Privacy Guard

The system scans for personally identifiable information.

Sensitive data is masked before further processing.

---

### Step 5 — Firewall

The firewall analyzes the request for malicious patterns such as:

* prompt injection attempts
* architecture probing
* system prompt extraction

Blocked requests are rejected.

---

### Step 6 — Routing

The routing module classifies user intent.

Possible outcomes include:

* deterministic response
* LLM reasoning request
* safety response

---

### Step 7 — Memory Retrieval

Conversation history is retrieved to maintain session continuity.

---

### Step 8 — Orchestration

The orchestrator prepares the final prompt and coordinates execution of the LLM request.

---

### Step 9 — LLM Processing

The request is sent to the Claude model hosted on AWS Bedrock.

The model generates a response.

---

### Step 10 — Response Validation

The validator ensures that the response:

* does not leak system prompts
* does not expose infrastructure details
* follows safety guidelines

---

### Step 11 — Logging

The system records structured events for monitoring and debugging.

Examples:

* request_received
* intent_classified
* routing_decision
* llm_request_started
* llm_request_completed

---

### Step 12 — Response Delivery

The validated response is returned to the frontend interface and displayed to the user.

---
