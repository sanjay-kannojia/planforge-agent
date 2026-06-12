# PlanForge

AI-powered Product Management agent that transforms business Epics into high-quality business Features using structured prompts, LangGraph workflows, AI-based evaluation, human review, targeted regeneration, and organizational learning.

---

# Vision

PlanForge helps Product Managers accelerate the planning process by converting business Epics into business-oriented Features that can be further decomposed into User Stories.

The long-term vision is to create an AI-assisted planning platform that:

* Generates Features from Epics
* Evaluates Feature quality
* Recommends approval actions
* Supports human review and approval
* Regenerates rejected Features using human feedback
* Learns from approved decomposition patterns
* Retrieves similar prior Epic decompositions
* Publishes approved artifacts to Confluence

---

# Problem Statement

Product Managers spend significant time decomposing business initiatives into Features and User Stories.

This process is often:

* Manual
* Inconsistent
* Dependent on individual experience
* Difficult to scale across teams

PlanForge aims to provide a repeatable, explainable, and AI-assisted planning workflow that reduces manual effort while preserving Product Manager judgment.

---

# Current Status

## Phase 1: Epic to Feature Decomposition

### Milestone Status

| Milestone                                        | Status     |
| ------------------------------------------------ | ---------- |
| Milestone 1 - Feature Generation                 | ✅ Complete |
| Milestone 2 - Feature Evaluation                 | ✅ Complete |
| Milestone 3 - Human Review & Regeneration        | ✅ Complete |
| Milestone 4 - Organizational Learning (ChromaDB) | ✅ Complete |
| Milestone 5 - Confluence Publishing              | ⬜ Planned  |

Current Version:

```text
v0.4.0
```

---

# Current Capabilities

PlanForge currently supports:

* Epic data capture
* AI-powered Feature Set generation
* Structured prompt engineering
* JSON-based Feature output
* Pydantic schema validation
* LangGraph workflow orchestration
* AI-based Feature evaluation
* Approval recommendation generation
* Evaluation findings generation
* Human review at the Feature level
* Feature approval
* Feature rejection with mandatory feedback
* Targeted regeneration of rejected Features
* Preservation of approved Features
* Feature version tracking during the current session
* ChromaDB-based organizational learning
* Similar Epic decomposition retrieval
* Rejected Feature lesson storage
* Retrieved learning context display
* Streamlit user interface

---

# Current Workflow

```text
Epic
  ↓
Retrieve Similar Epic Decomposition Patterns
  ↓
OpenAI Feature Set Generation
  ↓
Pydantic Schema Validation
  ↓
OpenAI Feature Set Evaluation
  ↓
Approval Recommendation + Findings
  ↓
Human Feature Review
  ↓
Approve or Reject
  ↓
Regenerate Rejected Features Only
  ↓
Re-evaluate Regenerated Features
  ↓
When All Features Are Approved
  ↓
Store Completed Learning Artifact in ChromaDB
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

## Feature Identity

Each Feature should have its own distinct business identity.

A Feature should be independently understandable, independently valuable, and independently decomposable into User Stories.

PlanForge avoids generating filler Features simply to reach a fixed count.

---

## Human Judgment Is Final

AI evaluates and recommends.

Humans approve or reject.

PlanForge is designed to reduce Product Manager effort, not replace Product Manager judgment.

---

## Rejection Requires Feedback

Approved Features do not require feedback.

Rejected Features require human feedback before regeneration.

Human feedback is the primary input for targeted regeneration.

---

## Preserve Approved Work

Approved Features remain unchanged during regeneration.

Only rejected Features are regenerated.

This allows Product Managers to improve weak Features without losing already-approved work.

---

## Learn From Completed Outcomes

PlanForge stores organizational learning only after the full Feature Set reaches approval.

Active review history remains in workflow/session state.

ChromaDB is used as a semantic learning repository, not as active workflow state.

---

# Technology Stack

| Component              | Technology    |
| ---------------------- | ------------- |
| UI                     | Streamlit     |
| Workflow Engine        | LangGraph     |
| LLM                    | OpenAI        |
| Schema Validation      | Pydantic      |
| Vector Store           | ChromaDB      |
| Environment Management | Python Dotenv |
| Language               | Python        |

Planned:

| Component                | Technology     |
| ------------------------ | -------------- |
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

Local-only files and folders:

```text
.env
chroma_db/
```

These must not be committed to GitHub.

---

# Environment Configuration

Create a local `.env` file using `.env.example` as the template.

Required variables:

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
OPENAI_TEMPERATURE=0.2

CHROMA_DB_PATH=./chroma_db
CHROMA_COLLECTION_EPIC_DECOMPOSITIONS=epic_decompositions
CHROMA_COLLECTION_REJECTED_FEATURE_LESSONS=rejected_feature_lessons
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
* Improve resource manager confidence in staffing recommendations

### Example Features Generated

* Resource Discovery
* Intelligent Resource Matching
* Staffing Recommendation Review and Adjustment
* Staffing Performance Analytics

---

# Example Evaluation Output

For each generated Feature, PlanForge provides:

* Evaluation Recommendation
* Findings

Example:

```text
Feature: Intelligent Resource Matching

Evaluation Recommendation:
APPROVE

Findings:
- Strong business-user-facing capability
- Directly supports the Epic objective
- Delivers measurable business value
```

---

# Example Human Review Flow

```text
Feature: Resource Manager Confidence Assessment

AI Recommendation:
REVIEW

Human Decision:
Reject

Human Feedback:
This is not a standalone Feature. It feels like a metric or supporting activity inside Staffing Recommendation Review.

PlanForge:
Regenerates only this rejected Feature.
Approved Features remain unchanged.
```

---

# Organizational Learning

PlanForge stores completed approved Epic-to-Feature decompositions in ChromaDB.

Stored learning artifacts include:

* Original Epic
* Final approved Feature Set
* Rejected Feature lessons
* Human rejection feedback
* AI evaluation findings
* Feature version history summary
* Regeneration history summary

PlanForge retrieves similar approved Epic decomposition patterns before generating Features for a new Epic.

It retrieves rejected Feature lessons during regeneration to avoid repeating prior mistakes.

---

# Sample Epics

PlanForge includes approved Epic-to-Feature decomposition examples under:

```text
sample_epics/
```

These examples represent Product Manager-approved decompositions and serve as reference patterns for future evaluation and organizational learning.

---

# Roadmap

## Milestone 5

Confluence Publishing

Capabilities:

* Publish approved Features
* Version tracking
* Approval audit trail
* Evaluation summary publishing
* Learning context summary publishing
* Confluence integration

---

# License

MIT License