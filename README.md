# PlanForge

AI-powered Product Management agent that transforms business Epics into high-quality business Features using structured prompts, LangGraph workflows, AI-based evaluation, and human approval.

---

# Vision

PlanForge helps Product Managers accelerate the planning process by converting business Epics into business-oriented Features that can be further decomposed into User Stories.

The long-term vision is to create an AI-assisted planning platform that:

* Generates Features from Epics
* Evaluates Feature quality
* Recommends approval actions
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

## Phase 1: Epic to Feature Decomposition

### Milestone Status

| Milestone                                        | Status      |
| ------------------------------------------------ | ----------- |
| Milestone 1 - Feature Generation                 | ✅ Complete  |
| Milestone 2 - Feature Evaluation                 | ⬜ In Design |
| Milestone 3 - Human Review & Regeneration        | ⬜ Planned   |
| Milestone 4 - Organizational Learning (ChromaDB) | ⬜ Planned   |
| Milestone 5 - Confluence Publishing              | ⬜ Planned   |

Current Version:

```text
v0.1.0
```

---

# Current Capabilities

PlanForge currently supports:

* Epic data capture
* AI-powered Feature generation
* Structured prompt engineering
* JSON-based Feature output
* Pydantic schema validation
* LangGraph workflow orchestration
* Streamlit user interface

Current workflow:

```text
Epic
  ↓
LangGraph Workflow
  ↓
OpenAI Feature Generation
  ↓
Pydantic Schema Validation
  ↓
Feature Display
```

---

# Design Principles

## Business Value First

A Feature should deliver meaningful business value.

Business value is more important than implementation details.

Examples:

### Strong Business Value

* Resource Discovery
* Intelligent Resource Matching
* Forecast Approval and Review
* Security Compliance Monitoring

### Weak Business Value

* Resource Database
* Matching Engine
* Forecast API

---

## Customer-Facing or Business-User-Facing

Generated Features should represent capabilities recognized by customers or business users.

Good:

* Resource Discovery
* Staffing Recommendation Review
* Regional Privacy Compliance Management

Poor:

* Resource Service
* Recommendation API
* Compliance Database

---

## Business Outcome Alignment

Every generated Feature should contribute directly to achieving the Epic objective.

Features that do not contribute to the desired business outcome should not be recommended.

---

## Human-in-the-Loop

AI generates recommendations.

Humans make approval decisions.

PlanForge is designed to reduce Product Manager effort, not replace Product Manager judgment.

---

# Technology Stack

| Component              | Technology    |
|------------------------|---------------|
| UI                     | Streamlit     |
| Workflow Engine        | LangGraph     |
| LLM                    | OpenAI        |
| Schema Validation      | Pydantic      |
| Environment Management | Python Dotenv |
| Language               | Python        |

Planned:

| Component                | Technology     |
| ------------------------ | -------------- |
| Feature Evaluation       | OpenAI         |
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
├── sample_epics/
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

# Sample Epics

PlanForge includes approved Epic-to-Feature decomposition examples under:

```text
sample_epics/
```

These examples represent Product Manager-approved decompositions and serve as reference patterns for future evaluation and organizational learning.

---

# Roadmap

## Milestone 2

Feature Evaluation and Approval Recommendation

Capabilities:

* AI-based Feature evaluation
* Business value assessment
* Outcome alignment assessment
* Business capability assessment
* Feature overlap detection
* Approval recommendation generation
* Improvement opportunity identification
* Regeneration guidance generation

---

## Milestone 3

Human Review and Regeneration

Capabilities:

* Feature approval workflow
* Feature rejection workflow
* Mandatory rejection feedback
* Targeted Feature regeneration
* Feature version management

---

## Milestone 4

Organizational Learning

Capabilities:

* ChromaDB integration
* Approved Feature storage
* Rejected Feature storage
* Rejection feedback storage
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