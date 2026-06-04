# PlanForge

AI-powered Product Management agent that transforms business Epics into high-quality business Features using structured prompts, LangGraph workflows, and human-in-the-loop review.

---

# Vision

PlanForge helps Product Managers accelerate the planning process by converting business Epics into business-oriented Features that can be further decomposed into User Stories.

The long-term vision is to create an AI-assisted planning platform that:

* Generates Features from Epics
* Validates Feature quality
* Supports human review and approval
* Learns from feedback over time
* Publishes approved artifacts to Confluence

---

# Problem Statement

Product Managers spend significant time decomposing business initiatives into Features and User Stories.

This process is often:

* Manual
* Inconsistent
* Dependent on individual experience
* Difficult to scale across teams

PlanForge aims to provide a repeatable, explainable, and AI-assisted planning workflow.

---

# Current Status

## Phase 1: Epic to Feature

### Milestone Status

| Milestone                                        | Status     |
| ------------------------------------------------ | ---------- |
| Milestone 1 - Feature Generation                 | ✅ Complete |
| Milestone 2 - Feature Validation                 | ⬜ Planned  |
| Milestone 3 - Human Review & Regeneration        | ⬜ Planned  |
| Milestone 4 - Organizational Learning (ChromaDB) | ⬜ Planned  |
| Milestone 5 - Confluence Publishing              | ⬜ Planned  |

Current Version:

```text
v0.1.0
```

---

# Current Capabilities

PlanForge currently supports:

* Epic data capture
* AI-powered Feature generation
* Structured JSON output
* Pydantic schema validation
* LangGraph workflow orchestration
* Streamlit user interface

Example flow:

```text
Epic
  ↓
LangGraph Workflow
  ↓
OpenAI Feature Generation
  ↓
Pydantic Validation
  ↓
Feature Display
```

---

# Design Principles

## Customer-Facing Features

PlanForge prioritizes generation of customer-facing or business-user-facing Features.

Example:

### Good

* Resource Discovery
* Intelligent Resource Matching
* Forecast Approval and Review

### Poor

* Resource Database
* Matching Engine
* Forecast API

---

## Business Outcome Alignment

Every generated Feature should contribute directly to the business outcome defined in the Epic.

---

## Human-in-the-Loop

AI generates recommendations.

Humans remain responsible for approval and final decisions.

---

# Technology Stack

| Component              | Technology    |
| ---------------------- | ------------- |
| UI                     | Streamlit     |
| Workflow Engine        | LangGraph     |
| LLM                    | OpenAI        |
| Validation             | Pydantic      |
| Environment Management | Python Dotenv |
| Language               | Python        |

Planned:

| Component                | Technology     |
| ------------------------ | -------------- |
| Vector Database          | ChromaDB       |
| Documentation Publishing | Confluence API |
| Observability            | LangSmith      |

---

# Repository Structure

```text
planforge/
│
├── app.py
│
├── docs/
│   ├── architecture/
│   ├── design/
│   ├── prd/
│   └── prompts/
│
├── src/
│   ├── graph/
│   ├── models/
│   ├── prompts/
│   ├── services/
│   └── state/
│
├── tests/
│
├── requirements.txt
│
└── .env.example
```

---

# Example Epic

## Epic

AI-Powered Resource Matching

### Business Objective

Provide intelligent recommendations for matching resources to projects.

### Success Metrics

* Reduce staffing effort by 30%
* Increase project fulfillment accuracy by 20%

### Example Features Generated

* Resource Discovery
* Intelligent Resource Matching
* Staffing Recommendation Review
* Match Explainability
* Staffing Performance Analytics

---

# Roadmap

## Milestone 2

Feature Validation Workflow

Capabilities:

* AI-based Feature review
* Business capability validation
* Business value validation
* Outcome alignment validation
* Feature overlap detection

---

## Milestone 3

Human Review and Regeneration

Capabilities:

* Feature approval workflow
* Feature rejection workflow
* Feedback capture
* Targeted Feature regeneration

---

## Milestone 4

Organizational Learning

Capabilities:

* ChromaDB integration
* Approved Feature storage
* Rejected Feature storage
* Similarity-based retrieval
* Feedback-informed generation

---

## Milestone 5

Confluence Publishing

Capabilities:

* Publish approved Features
* Version tracking
* Approval audit trail
* Confluence integration

---

# License

MIT License