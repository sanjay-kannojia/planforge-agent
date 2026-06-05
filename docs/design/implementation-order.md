# PlanForge

# Implementation Order

This document defines the implementation sequence for PlanForge and identifies the authoritative source documents for each milestone.

The purpose of this document is to provide clear guidance to developers, AI coding assistants, and future contributors regarding:

* What should be built next
* Which documents should be used as the source of truth
* Which milestones are complete
* Which milestones remain future work

| Document     | Purpose                   |
| ------------ | ------------------------- |
| PRD          | What to build             |
| Architecture | Where it fits             |
| Design       | How it works              |
| Prompt       | How the LLM behaves       |
| Sample Epics | Examples of good outcomes |
---

# Phase 1: Epic to Feature Decomposition

---

## Milestone 1

### Status

✅ Complete

### Objective

Generate business Features from a business Epic.

### Source Documents

#### Business Requirements

* docs/prd/epic-to-feature-prd.md

#### Architecture

* docs/architecture/phase1-architecture.md

#### Design

* docs/design/milestone-1-design.md

#### Prompts

* docs/prompts/feature-generation-prompt.md

### Deliverables

* Epic Intake
* Feature Generation
* Pydantic Schema Validation
* Streamlit User Interface
* LangGraph Workflow

---

## Milestone 2

### Status

🚧 Next

### Objective

Evaluate generated Features and provide approval recommendations prior to human review.

### Source Documents

#### Business Requirements

* docs/prd/epic-to-feature-prd.md

#### Architecture

* docs/architecture/phase1-architecture.md

#### Design

* docs/design/milestone-2-design.md

#### Prompts

* docs/prompts/feature-evaluation-prompt.md

#### Reference Examples

* sample_epics/

### Deliverables

* Feature Evaluation
* Approval Recommendation
* Findings Generation
* Improvement Opportunity Generation
* Regeneration Guidance Generation
* Evaluation Results UI

### Implementation Rules

* Preserve all Milestone 1 functionality.
* Follow milestone-2-design.md as the primary implementation guide.
* Do not implement Human Review workflows.
* Do not implement Feature Regeneration.
* Do not implement ChromaDB integration.
* Do not implement Confluence integration.

---

## Milestone 3

### Status

🔮 Future

### Objective

Enable human review, approval, rejection, and targeted Feature regeneration.

### Planned Capabilities

* Feature Approval
* Feature Rejection
* Mandatory Rejection Feedback
* Targeted Feature Regeneration
* Feature Version Tracking

---

## Milestone 4

### Status

🔮 Future

### Objective

Introduce organizational learning and retrieval using ChromaDB.

### Planned Capabilities

* ChromaDB Integration
* Approved Feature Storage
* Rejected Feature Storage
* Human Feedback Storage
* Similarity-Based Retrieval
* Feedback-Informed Generation

---

## Milestone 5

### Status

🔮 Future

### Objective

Publish approved Features to Confluence.

### Planned Capabilities

* Confluence Publishing
* Approval Metadata
* Version History
* Audit Trail

---

# Implementation Guidance for AI Coding Assistants

When implementing a milestone:

1. Read the PRD first.
2. Read the Architecture document second.
3. Read the milestone Design document third.
4. Read the Prompt document fourth.
5. Review sample_epics as reference examples.
6. Implement only the current milestone.
7. Do not implement future milestones unless explicitly instructed.

Current Implementation Target:

Milestone 2 - Feature Evaluation and Approval Recommendation