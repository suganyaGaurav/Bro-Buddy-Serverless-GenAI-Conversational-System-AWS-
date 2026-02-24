# Bro-Buddy – Serverless GenAI Conversational System (AWS)

AWS serverless LLM inference system with explicit prompt governance, IAM-restricted Bedrock access, cost-aware model configuration, behavioral mode architecture, and observability-driven design.

---

## Overview

Bro-Buddy is a production-oriented serverless GenAI inference pipeline built on AWS.

The system demonstrates controlled LLM invocation using Amazon Bedrock with:

- Enforced inference profile validation  
- IAM-scoped model permissions  
- Cost-bounded generation parameters  
- Governance-aware prompt construction  
- Mode-separated conversational behavior  

The architecture is intentionally minimal, secure, and scalable.

---

## Architecture

Static Frontend  
→ API Gateway  
→ AWS Lambda (Python 3.x)  
→ Amazon Bedrock (Inference Profile ARN)  
→ Foundation Model  
→ Response returned via API Gateway  

### Supporting Components

- IAM Least Privilege Execution Role  
- CloudWatch Logging  
- Environment-Based Model Configuration  

No EC2  
No RDS  
No Containers  

Pure serverless inference pipeline.

---

## Conversational Mode Architecture

Bro-Buddy implements explicit behavioral separation using controlled conversational modes.

Each mode enforces a distinct response framework at the prompt level to ensure clarity, governance alignment, and predictable output style.

### Default Mode: Professional Bro (Calm Mentor)

Professional Bro is the default execution mode.

**Purpose**

Provide structured guidance for:
- Career development  
- Learning roadmaps  
- Performance concerns  
- Technical concept clarification  
- Professional decision-making  

**Behavioral Characteristics**

- Offers structured direction instead of instant solutions  
- Provides conceptual guidance rather than copy-paste production code  
- Presents balanced trade-offs instead of making decisions  
- Asks at most one focused clarification question  
- Maintains a calm, mentor-like tone  

**Boundaries**

- No direct production-ready code generation  
- No tactical execution scripts  
- No medical, legal, or financial advice  

---

### Chill Bro (Warm Companion Mode)

Chill Bro is designed for lighter conversations.

**Purpose**

- Everyday chats  
- Emotional processing  
- Casual discussions  
- Movies, ideas, general topics  

**Behavioral Characteristics**

- Validates emotion before offering perspective  
- Keeps responses concise and warm  
- Avoids structured career frameworks  
- Redirects professional guidance to Professional mode when necessary  

This separation ensures behavioral clarity and prevents cross-mode contamination.

---

## Memory Design

Bro-Buddy uses session-level conversational memory.

- Conversation history is maintained per browser session  
- Memory resets when switching modes  
- Memory window is capped (last N messages) to control cost and drift  
- No persistent database storage in current scope  

This provides contextual continuity without adding infrastructure complexity.

---

## Key Design Decisions

### 1. Cost-Controlled Model Strategy

- Bedrock inference profile required (no direct base model usage)  
- Maximum tokens capped at 150  
- Temperature set to 0.3 for stable responses  
- Environment-based configuration for deployment flexibility  

This ensures predictable cost behavior and controlled model access.

---

### 2. Governance-First Prompting

- Explicit boundary enforcement (no medical or legal advice)  
- Mode-based tone switching  
- Clear separation of system and user messages  
- Identity lock enforcement  
- Fail-fast configuration validation  

The system prevents accidental misconfiguration and enforces approved inference paths.

---

### 3. IAM Restriction (Least Privilege)

Lambda execution role limited to:

- `bedrock:InvokeModel` (scoped to inference profile ARN)  
- `logs:CreateLogStream`  
- `logs:PutLogEvents`  

No unnecessary service permissions.

---

### 4. Runtime Safeguards

- Fails immediately if `MODEL_ID` environment variable is missing  
- Validates ARN format to enforce inference profile usage  
- Prevents direct model ID invocation  
- Lightweight imports to reduce Lambda cold start latency  

---

### 5. Observability

- CloudWatch logging for invocation tracing  
- Structured error handling  
- Explicit exception propagation  
- Request-level debugging visibility  

The system supports traceability for:

- API failures  
- Invocation errors  
- Unexpected model behavior  

---

## Deployment

- Runtime: Python 3.x  
- Trigger: API Gateway  
- Execution: AWS Lambda  

### Required Environment Variable

`MODEL_ID`  
Must contain a valid Bedrock inference profile ARN.

### Required IAM Permissions

- `bedrock:InvokeModel` (scoped to inference profile ARN)  
- `logs:CreateLogStream`  
- `logs:PutLogEvents`  

---

## Current Scope

This repository focuses strictly on:

- Secure model invocation  
- Governance enforcement  
- Mode-based conversational behavior  
- Serverless cost control  
- Observability readiness  

It is intentionally minimal to demonstrate architectural clarity rather than feature complexity.

---

## Future Enhancements

- Structured latency logging  
- Token usage accounting  
- RAG integration layer  
- Persistent conversation memory  
- Expanded governance auditing  
- Frontend telemetry metrics  

---

## Author

Built and designed by Suganya.

---

Serverless. Governance-aware. Cost-controlled. Mode-separated. Observability-ready.
