# Bro-Buddy-Serverless-GenAI-Conversational-System-AWS-
AWS serverless LLM inference system with explicit prompt governance, IAM-restricted Bedrock access, cost-aware model configuration, and observability-driven design.

Overview

Bro-Buddy is a production-oriented serverless GenAI inference pipeline built on AWS. 
The system demonstrates controlled LLM invocation using Amazon Bedrock with:

* Enforced inference profile validation
* IAM-scoped model permissions
* Cost-bounded generation parameters
* Governance-aware prompt construction

The architecture is intentionally minimal, secure, and scalable.

Architecture
Static Frontend
→ API Gateway
→ AWS Lambda (Python)
→ Amazon Bedrock (Inference Profile)
→ Foundation Model
→ Response returned via API Gateway

Supporting Components

-> IAM Least Privilege Execution Role
-> CloudWatch Logging
-> Environment-Based Model Configuration

No EC2
No RDS
No Containers

Key Design Decisions

1. Cost-Controlled Model Strategy 
  * Bedrock inference profile required (no direct base model usage)
  * Maximum tokens capped at 150
  * Temperature set to 0.3 for stable responses
  * Environment-based configuration for deployment flexibility
This ensures predictable cost behavior and controlled model access.

2. Governance-First Prompting
  * Explicit boundary enforcement (no medical or legal advice)
  * Mode-based tone switching
  * Clear separation of system and user messages
  * Fail-fast configuration validation
The system prevents accidental misconfiguration and enforces approved inference paths.

3. IAM Restriction (Least Privilege)
  * Lambda execution role limited to:
  * bedrock:InvokeModel (scoped to inference profile ARN)
  * logs:CreateLogStream
  * logs:PutLogEvents
No unnecessary service permissions.

4. Runtime Safeguards
  * Fails immediately if MODEL_ID environment variable is missing
  * Validates ARN format to enforce inference profile usage
  * Prevents direct model ID invocation
  * Lightweight imports to reduce Lambda cold start latency

5. Observability
  * CloudWatch logging for invocation tracing
  * Structured error handling
  * Explicit exception propagation
  * Request-level debugging visibility

Deployment
  * Runtime: Python 3.x
  * Trigger: API Gateway
  * Execution: AWS Lambda

Required Environment Variable
  * MODEL_ID
Must contain a valid Bedrock inference profile ARN.

Required IAM Permissions
  * bedrock:InvokeModel (scoped to inference profile ARN)
  * logs:CreateLogStream
  * logs:PutLogEvents

Current Scope
This repository focuses strictly on:
  * Secure model invocation
  * Governance enforcement
  * Serverless cost control
  * Observability readiness
It is intentionally minimal to demonstrate architectural clarity rather than feature complexity.

Future Enhancements
  * Structured latency logging
  * Token usage accounting
  * RAG integration layer
  * Conversation memory system
  * Expanded governance auditing

Pure serverless inference pipeline.
