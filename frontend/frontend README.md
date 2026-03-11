# Frontend — Bro-Buddy UI

## Overview

This folder contains the **user interface for the Bro-Buddy AI companion system**.

The frontend is intentionally lightweight and built using **pure HTML and CSS**.
It provides a simple chat interface that allows users to interact with the backend AI pipeline.

The UI captures user input and sends it to the backend API, where the AI processing pipeline handles routing, guardrails, and model responses.

---

## Files

### index.html

Main UI page that renders the chat interface.

Responsibilities:

* Displays the chat window
* Accepts user input
* Sends prompts to the backend API
* Displays responses from the AI system

---

### style.css

Provides styling for the chat interface.

Responsibilities:

* Chat layout styling
* Message bubble formatting
* Responsive design
* Typography and spacing

---

## User Interaction Flow

User types a message in the chat interface
↓
index.html captures the message
↓
Frontend sends request to backend API
↓
AWS Lambda backend processes request
↓
AI model generates response
↓
Response returned to frontend
↓
Chat message displayed to the user

---

## Design Philosophy

The frontend intentionally avoids heavy frameworks such as React or Vue.

Reasons:

* Keeps deployment simple
* Reduces build complexity
* Focuses the project on **AI system architecture rather than frontend frameworks**

This allows the project to emphasize:

* AI routing
* guardrails
* prompt governance
* evaluation testing

---

## Future Improvements

Planned UI improvements may include:

* Streaming AI responses
* Typing indicator
* Chat history persistence
* Mobile responsiveness
* Dark mode support

---

## Related Backend Components

The frontend connects to the backend AI system which includes:

* Request handler
* Capacity guard
* Privacy guard
* Prompt firewall
* Intent routing
* Memory module
* LLM client
* Response validator
* Structured logging

These components ensure responses are **safe, controlled, and observable**.

---

## Project Purpose

This project demonstrates how a **governance-first AI system** can be designed and evaluated using production-style architecture and safety guardrails.
