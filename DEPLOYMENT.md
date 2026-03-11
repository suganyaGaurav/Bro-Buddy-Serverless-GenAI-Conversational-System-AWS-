# Bro-Buddy Deployment Guide

## Live Deployment

Frontend (GitHub Pages)

https://suganyagaurav.github.io/Bro-Buddy-Serverless-GenAI-Conversational-System-AWS/

Backend API (AWS API Gateway)

https://******************.amazonaws.com/dev/chat

---

# Deployment Architecture

Bro-Buddy is deployed using a **serverless AI architecture on AWS**.

```
User Browser
     │
     ▼
GitHub Pages (Frontend UI)
     │
     ▼
API Gateway
     │
     ▼
AWS Lambda
     │
     ▼
Bro-Buddy AI Pipeline
     │
     ▼
Amazon Bedrock Claude
```

---

# Infrastructure Components

### Frontend

* Static HTML + CSS UI
* Hosted using **GitHub Pages**
* Provides chat interface and mode switching

### API Gateway

* Public API endpoint for the chatbot
* Handles routing of frontend requests to Lambda

### AWS Lambda

Main backend orchestration layer containing:

* handler.py
* routing.py
* firewall.py
* privacy_guard.py
* memory_store.py
* orchestrator.py
* validator.py

### Amazon Bedrock

LLM inference using **Claude model**.

Used only when routing determines reasoning is required.

---

# Governance Layers

Bro-Buddy includes multiple safety layers before LLM execution.

1. Capacity Guard
   Prevents excessive request traffic.

2. Privacy Guard
   Masks sensitive data such as emails.

3. Firewall
   Blocks adversarial or unsafe prompts.

4. Routing
   Determines deterministic vs LLM path.

5. Validator
   Prevents prompt leakage or infrastructure disclosure.

6. Observability Logs
   Structured logging using CloudWatch.

---

# Deployment Steps

### Step 1 — Deploy Backend

1. Create Lambda function
2. Upload backend modules
3. Configure IAM access for Bedrock
4. Connect Lambda to API Gateway

### Step 2 — Enable CORS

Allow frontend origin:

```
https://suganyagaurav.github.io
```

Allowed methods:

```
POST
OPTIONS
```

### Step 3 — Deploy Frontend

Frontend UI hosted via GitHub Pages.

Settings → Pages
Source → main branch
Folder → root

---

# Monitoring

System monitoring is handled via:

CloudWatch Logs

Captured events include:

* request_received
* firewall_checked
* routing_decision
* llm_request_started
* llm_request_completed
* memory_updated

This provides **full observability of the AI pipeline**.

---

# Current Version

Bro-Buddy v1.0

Features:

* governance-aware conversational AI
* deterministic routing
* memory support
* firewall protection
* prompt governance
* AWS serverless deployment

---

# Future Improvements

Planned enhancements:

* semantic prompt injection detection
* expanded PII detection
* improved greeting routing coverage
* evaluation automation

---

© Suganya
Governance-First AI Systems
