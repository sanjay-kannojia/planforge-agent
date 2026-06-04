# PlanForge

## Phase 1 Architecture

**Document Version:** 4.1

---

# 1. Architecture Objective

PlanForge transforms a business Epic into a validated and approved Feature Set through AI-assisted decomposition, human review, organizational learning, and enterprise publishing.

The architecture demonstrates:

* AI-powered decomposition
* Human-in-the-loop review
* Feature-level approvals
* Targeted regeneration
* Organizational learning
* Enterprise integration
* Workflow observability

---

# 2. Architectural Principles

## AP1 - Human Approval Required

No generated Feature may be published without explicit human approval.

---

## AP2 - Feedback-Driven Improvement

A rejected Feature must include reviewer feedback.

Regeneration is not permitted without feedback.

---

## AP3 - Preserve Approved Work

Approved Features remain unchanged during regeneration cycles.

Only rejected Features are regenerated.

---

## AP4 - Organizational Learning

The system learns from previously approved and rejected artifacts to improve future decomposition quality.

---

## AP5 - Traceability

Every generation, review, approval, rejection, and publication action must be traceable.

---

## AP6 - Extensibility

The architecture must support future decomposition phases:

Epic
  ↓
Feature
  ↓
User Story
  ↓
Backlog Item

without major redesign.

---

# 3. High-Level Architecture

┌─────────────────┐
│    Streamlit    │
│       UI        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    LangGraph    │
│ Workflow Engine │
└────────┬────────┘
         │
         ▼
 ┌─────────────────────┐
 │ Knowledge Retrieval │
 └──────────┬──────────┘
            │
            ▼
 ┌─────────────────────┐
 │ Feature Generation  │
 └──────────┬──────────┘
            │
            ▼
 ┌─────────────────────┐
 │ Feature Validation  │
 └──────────┬──────────┘
            │
            ▼
 ┌─────────────────────┐
 │  Feature Review UI  │
 └──────────┬──────────┘
            │
      ┌─────┴─────┐
      │           │
      ▼           ▼
 Approved     Rejected
      │           │
      │      Feedback
      │           │
      │           ▼
      │    Regeneration
      │           │
      └─────┬─────┘
            │
            ▼
      All Approved?
            │
            ▼
     Confluence Publish
            │
            ▼
     Organizational Store

---

# 4. Technology Stack

| Layer           | Technology     | Purpose                               |
| --------------- | -------------- | ------------------------------------- |
| UI              | Streamlit      | User interaction                      |
| Workflow        | LangGraph      | State management and orchestration    |
| LLM             | OpenAI GPT     | Feature generation and revision       |
| Validation      | Pydantic       | Schema enforcement                    |
| Knowledge Store | ChromaDB       | Organizational learning and retrieval |
| Publishing      | Confluence API | Enterprise publishing                 |
| Observability   | LangSmith      | Workflow tracing                      |

---

# 5. Workflow Nodes

## Node 1 - Epic Intake

### Inputs

* Epic Title
* Epic Description
* Business Context
* Success Metrics

### Outputs

* Epic Object

### Milestone

Milestone 1

---

## Node 2 - Knowledge Retrieval

### Purpose

Retrieve historical artifacts to improve generation quality.

### Inputs

* Epic

### Outputs

* Similar Approved Features
* Similar Approved Feature Sets
* Similar Rejected Features
* Associated Reviewer Feedback

### Milestone

Milestone 5

---

## Node 3 - Feature Generation

### Inputs

* Epic
* Retrieved Context (optional)

### Outputs

* Generated Feature Set

### Milestone

Milestone 1

---

## Node 4 - Feature Validation

### Inputs

* Generated Feature Set

### Outputs

* Validated Feature Set

### Milestone

Milestone 2

---

## Node 5 - Feature Review

### Inputs

* Validated Feature Set

### Outputs

* Feature Decisions
* Reviewer Feedback

### Business Rules

* Feedback is mandatory for rejected Features.
* Approved Features cannot be modified automatically.

### Milestone

Milestone 3

---

## Node 6 - Feature Regeneration

### Inputs

* Rejected Features
* Reviewer Feedback
* Retrieved Context

### Outputs

* Revised Features

### Business Rules

* Only rejected Features are regenerated.
* Approved Features remain unchanged.

### Milestone

Milestone 3

---

## Node 7 - Confluence Publisher

### Inputs

* Approved Feature Set

### Outputs

* Published Artifact

### Milestone

Milestone 4

---

## Node 8 - Organizational Learning Writer

### Inputs

* Feature Set
* Feature Decisions
* Reviewer Feedback
* Approval Outcome

### Outputs

* Stored Artifacts

### Milestone

Milestone 5

---

# 6. Data Model

## Epic

```python
Epic
{
  title
  description
  business_context
  success_metrics
}
```

---

## Feature

```python
Feature
{
  feature_id
  name
  description
  business_value
  acceptance_criteria
  approval_status
  reviewer_feedback
  version
}
```

---

## Feature Set

```python
FeatureSet
{
  epic_id
  features[]
  version
}
```

---

# 7. Organizational Learning Model

## Approved Feature Artifacts

Store:

* Feature
* Epic Context
* Approval Metadata

Purpose:

Provide successful examples for future generation.

---

## Rejected Feature Artifacts

Store:

* Rejected Feature Version
* Reviewer Feedback
* Rejection Metadata
* Version Number

Purpose:

Preserve learning signals and reviewer intent.

### Prototype Constraint

Store a maximum of four rejected versions per Feature.

Example:

Feature C v1 → Rejected
Feature C v2 → Rejected
Feature C v3 → Rejected
Feature C v4 → Rejected
Feature C v5 → Rejected
Feature C v6 → Approved

Repository stores:

v2
v3
v4
v5
v6 (Approved)

Oldest rejected versions are removed when retention limits are exceeded.

---

## Feature Set Artifacts

Store:

* Epic
* Feature Set
* Approval Outcome
* Publication Metadata

Purpose:

Support decomposition pattern retrieval.

---

# 8. Retrieval Strategy

## Initial Generation

Retrieve:

* Similar Approved Feature Sets
* Similar Approved Features

Purpose:

Improve generation quality.

---

## Regeneration

Retrieve:

* Current Rejected Feature
* Reviewer Feedback
* Similar Approved Features
* Similar Rejected Features with Feedback

Purpose:

Improve targeted revisions.

---

# 9. State Management

LangGraph state contains:

```python
{
  epic,
  feature_set,
  feature_decisions,
  reviewer_feedback,
  validation_results,
  version_history,
  retrieved_context,
  publication_status
}
```

---

# 10. Version Management

Feature-level versioning is required.

Example:

Feature A v1 → Approved

Feature B v1 → Approved

Feature C v1 → Rejected
Feature C v2 → Rejected
Feature C v3 → Approved

Feature Set version history is also maintained.

---

# 11. Observability

Track:

* Node execution
* State transitions
* Validation outcomes
* Retrieval activity
* Approval decisions
* Regeneration cycles
* Publication events

---

# 12. Implementation Mapping

| Milestone   | Capability                          |
| ----------- | ----------------------------------- |
| Milestone 1 | Epic → Feature Generation           |
| Milestone 2 | Feature Validation                  |
| Milestone 3 | Feature-Level Review & Regeneration |
| Milestone 4 | Confluence Publishing               |
| Milestone 5 | Organizational Learning & Retrieval |

---

# 13. Future Extensions

* User Story generation
* Backlog Item generation
* Advanced RAG
* Multi-reviewer workflows
* Jira integration
* Additional enterprise integrations
* Relational persistence layer for workflow history and auditability