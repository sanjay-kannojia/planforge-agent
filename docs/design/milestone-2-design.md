# PlanForge

# Milestone 2 Design Document

## Phase 1: Epic to Feature Decomposition

## Milestone 2: Feature Evaluation and Approval Recommendation

---

# Document Status

# Change Log

## Version 2.1

Changes:

- Removed Improvement Opportunities from evaluation output.
- Simplified evaluation results to Recommendation and Findings.
- Clarified Milestone 3 consumption model.
- Aligned evaluation workflow with human approval and rejection process.

## Version 2.0

Initial Feature Evaluation and Approval Recommendation design.

---

# 1. Objective

Milestone 2 introduces AI-based Feature Evaluation.

The goal is to reduce Product Manager review effort by evaluating generated Features and providing approval recommendations before human review.

The system does not replace Product Manager judgment.

The system acts as an experienced Product Manager reviewer and performs an initial quality assessment of generated Features.

---

# 2. Business Problem

Feature generation alone does not guarantee quality.

Generated Features may:

* Be too technical
* Be too broad
* Be too narrow
* Overlap with another Feature
* Fail to support the Epic objective
* Deliver insufficient business value

Product Managers should not have to manually analyze every generated Feature from scratch.

The AI should perform an initial quality review and highlight potential concerns.

---

# 3. Scope

## In Scope

* Evaluate generated Features
* Assess Feature quality
* Generate approval recommendations
* Generate findings
* Generate improvement opportunities
* Display evaluation results in the UI
* Evaluate Features independently

## Out of Scope

* Human approval workflow
* Human rejection workflow
* Feature regeneration
* ChromaDB integration
* Confluence publishing
* User Story generation

These capabilities will be introduced in future milestones.

---

# 4. Evaluation Principles

The evaluator acts as an experienced Product Manager.

The evaluator focuses on:

* Business value
* User value
* Outcome alignment
* Feature quality
* Feature clarity

The evaluator does not evaluate:

* Architecture
* Technical implementation
* Coding approaches
* Infrastructure decisions

---

# 5. Evaluation Criteria

## 5.1 Business Value

### Question

Does the Feature create meaningful business value?

### Examples

Good:

* Reduce staffing effort
* Improve compliance
* Increase forecasting accuracy

Weak:

* Administrative activity with unclear value
* Technical capability without measurable outcome

### Priority

Highest

---

## 5.2 Outcome Alignment

### Question

Does the Feature directly contribute to achieving the Epic objective?

### Examples

Epic:

AI-Powered Resource Matching

Good:

Intelligent Resource Matching

Weak:

User Theme Configuration

### Priority

High

---

## 5.3 Business Capability

### Question

Does the Feature represent a customer-facing or business-user-facing capability?

### Examples

Good:

* Resource Discovery
* Security Compliance Monitoring
* Forecast Approval and Review

Weak:

* Resource Database
* Forecast Engine
* Authentication API

### Priority

High

---

## 5.4 Scope Appropriateness

### Question

Is the Feature appropriately sized?

The Feature should not represent:

* An Epic
* A User Story
* A Technical Task

### Priority

Medium

---

## 5.5 Feature Uniqueness

### Question

Does the Feature significantly overlap with another generated Feature?

### Priority

Medium

---

# 6. Evaluation Output

The evaluator generates:

* Recommendation
* Findings

The evaluator may calculate internal scores to support consistency.

Internal scores are not displayed to users.

---

# 7. Recommendation Types

## APPROVE

The Feature is likely acceptable for Product Manager approval.

Characteristics:

* Strong business value
* Clear Epic alignment
* Appropriate scope
* Minimal overlap

---

## REVIEW

The Feature may require Product Manager attention.

Characteristics:

* Moderate concerns
* Potential overlap
* Scope uncertainty
* Business value needs clarification

---

# 8. Evaluation Output Model

Example:

```json
{
  "feature_name": "Resource Discovery",
  "recommendation": "APPROVE",
  "findings": [
    "Strong business-user-facing capability.",
    "Directly supports staffing outcomes.",
    "Provides measurable business value."
  ]
}
```

Review Example:

```json
{
  "feature_name": "Resource Profile Management",
  "recommendation": "REVIEW",
  "findings": [
    "Appears to be a supporting capability.",
    "Business value is indirect."
  ]
}
```

---

# 9. Workflow

```text
Epic
↓
Feature Generation
↓
Feature Evaluation
↓
Approval Recommendation
↓
Display Results
```

---

# 10. LangGraph Flow

## Milestone 1

```text
Epic Intake
↓
Feature Generation
↓
Display Results
```

## Milestone 2

```text
Epic Intake
↓
Feature Generation
↓
Feature Evaluation
↓
Display Results
```

---

# 11. User Interface

For each generated Feature display:

## Feature Name

## Recommendation

Examples:

* APPROVE
* REVIEW

## Findings

Examples:

* Strong business value
* Strong Epic alignment
* Appropriate scope

### Example

Feature: Resource Discovery

Recommendation:

APPROVE

Findings:

* Strong business-user-facing capability
* Directly supports staffing outcomes
* Delivers measurable business value

---

### Example

Feature: Resource Profile Management

Recommendation:

REVIEW

Findings:

* Appears to be a supporting capability
* Business value is indirect

---

# 12. Human Interaction Model

The Product Manager is not expected to score Features.

The Product Manager reviews AI recommendations and prepares for future approval or rejection workflows.

Human approval and rejection actions are introduced in Milestone 3.

---

# 13. Benchmark Evaluation

Evaluation decisions should be informed by approved decomposition examples stored under:

```text
sample_epics/
```

These examples represent approved Product Manager decompositions and serve as reference patterns for quality evaluation.

---

# 14. Expected Implementation Artifacts

## New Files

```text
src/
│
├── graph/
│   └── evaluation_node.py
│
├── models/
│   ├── feature_evaluation.py
│   └── evaluation_result.py
│
├── services/
│   └── feature_evaluation_service.py
│
├── prompts/
│   └── feature_evaluation.py
```

---

## Updated Files

```text
app.py

src/
│
├── graph/
│   └── workflow.py

src/
│
└── state/
    └── workflow_state.py
```

---

## Repository Structure After Milestone 2

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
│   │
│   ├── graph/
│   │   ├── workflow.py
│   │   └── evaluation_node.py
│   │
│   ├── models/
│   │   ├── epic.py
│   │   ├── feature.py
│   │   ├── feature_set.py
│   │   ├── feature_evaluation.py
│   │   └── evaluation_result.py
│   │
│   ├── prompts/
│   │   ├── feature_generator.py
│   │   └── feature_evaluation.py
│   │
│   ├── services/
│   │   ├── llm_service.py
│   │   └── feature_evaluation_service.py
│   │
│   └── state/
│       └── workflow_state.py
│
├── tests/
│
├── requirements.txt
│
└── .env.example
```

---

# 15. Acceptance Criteria

## Functional

* Evaluate every generated Feature
* Produce approval recommendations
* Generate findings
* Display evaluation results in the UI

## User Experience

* Recommendations visible in Streamlit UI
* Findings easy to understand
* Weak Features easy to identify
* Product Manager review effort reduced

---

# 16. Explicitly Out of Scope

Do NOT implement:

* Human Approval Workflow
* Human Rejection Workflow
* Feature Regeneration
* ChromaDB Integration
* Confluence Publishing
* User Story Generation

These capabilities belong to future milestones.

---

# 17. Future Integration

## Milestone 3

Consumes:

* Evaluation Recommendations
* Findings
* Human Rejection Feedback

## Milestone 4

Stores:

* Approved Features
* Rejected Features
* AI Recommendations
* Human Feedback
* Regeneration History

## Milestone 5

Publishes:

* Approved Features
* Approval Metadata
* Evaluation Summary