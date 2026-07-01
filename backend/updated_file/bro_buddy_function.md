BroBuddy Chatbot – End-to-End Architecture Summary
1. User Request Received
User submits a query through the chatbot UI.
A unique request_id is generated.
Request metadata (timestamp, environment, model version) is initialized.

3. Request Validation
Validate request format.
Check for empty or invalid input.
Store query preview and input length.
Determine selected chatbot mode (Professional / AI).

5. Capacity Guard
Check current active requests.
Prevent overload by enforcing concurrency limits.
Allow or reject requests based on system capacity.

7. Governance Firewall
Scan user input against predefined safety rules.
Detect unsafe, malicious, or restricted content.
Block requests if policy violations are found.

9. Intent Classification
Classify user intent using deterministic routing logic.
Examples:
Greeting
Professional Reasoning
AI Knowledge
General Conversation
10. Routing Engine
Decide whether the request:
Can be answered deterministically, or
Requires LLM reasoning.
Prevent unnecessary LLM invocations to optimize cost and latency.

12. Prompt Preparation
Build the system prompt based on:
Selected mode
User query
Governance rules
Conversation history

14. LLM Invocation
Send the prepared prompt to AWS Bedrock.
Invoke Anthropic Claude Haiku model.
Measure request latency and response statistics.
15. Response Validation
Validate generated response.
Ensure output aligns with governance policies.
Prevent unsupported or unsafe responses.
16. Conversation Memory Update
Store the latest interaction.
Update session history.
Maintain conversational context for future requests.
17. Structured Logging & Observability

Capture detailed telemetry throughout the request lifecycle, including:

Request ID
Event timestamps
Intent
Routing decisions
Model used
LLM latency
Total request latency
Response statistics
System events

12. Response Delivery
Return the validated response to the user.
Log the completion of the request.

13. Resource Cleanup
Release active request count.
Complete request lifecycle.
Prepare the system for the next incoming request.

High-Level Workflow : 

User
   │
   ▼
Chat UI
   │
   ▼
Request Validation
   │
   ▼
Capacity Guard
   │
   ▼
Governance Firewall
   │
   ▼
Intent Classification
   │
   ▼
Routing Engine
   │
   ▼
Prompt Preparation
   │
   ▼
AWS Bedrock (Claude)
   │
   ▼
Response Validation
   │
   ▼
Conversation Memory
   │
   ▼
Structured Logging
   │
   ▼
User Response
   │
   ▼
Resource Cleanup

Key Engineering Highlights:

* Governance-first AI workflow
* Deterministic intent routing
* Controlled LLM invocation
* Structured JSON telemetry
* End-to-end request traceability
* Capacity and concurrency management
* AI observability with latency monitoring
* Conversation memory management
* Modular, production-inspired architecture
Explainable and auditable request lifecycle

This architecture demonstrates a complete AI request lifecycle rather than a simple chatbot, emphasizing reliability, governance, and operational visibility.
