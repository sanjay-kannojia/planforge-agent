# PlanForge

# Milestone 3 Design Document

## Phase 1: Epic to Feature Decomposition

## Milestone 3: Human Review and Targeted Feature Regeneration

---

# Document Status

Version 1.0

---

# 1. Objective

Milestone 3 introduces human-in-the-loop Feature review.

The goal is to allow a Product Manager to approve or reject each generated Feature after AI evaluation.

Approved Features are preserved.

Rejected Features require human feedback and are regenerated individually.

The system must regenerate only rejected Features while keeping approved Features unchanged.

---

# 2. Business Problem

AI-generated Features may not always meet Product Manager expectations.

Even after AI evaluation, a human Product Manager may determine that a Feature:

* Lacks sufficient business value
* Does not align with the Epic objective
* Is too broad
* Is too narrow
* Overlaps with another Feature
* Is not customer-facing or business-user-facing
* Feels like a supporting activity rather than a standalone Feature

Product Managers should not need to regenerate the entire Feature Set when only one Feature is weak.

PlanForge should support targeted improvement of rejected Features while preserving approved work.

---

# 3. Scope

## In Scope

* Human review of each generated Feature
* Feature-level approval
* Feature-level rejection
* Mandatory feedback for rejected Features
* Targeted regeneration of rejected Features
* Preservation of approved Features
* Re-evaluation of regenerated Features
* Feature version tracking within the current session
* Updated Streamlit UI for review decisions

## Out of Scope

* ChromaDB integration
* Confluence publishing
* Multi-reviewer workflows
* Role-based access control
* Persistent database storage
* User Story generation
* Backlog Item generation

These capabilities belong to future milestones.

---

# 4. Review Principles

## Human Judgment Is Final

AI evaluation provides recommendations and findings.

The Product Manager makes the approval decision.

---

## Approval Requires No Feedback

If a Feature is approved, no feedback is required.

Approval means the Product Manager accepts the Feature as useful for downstream planning.

---

## Rejection Requires Feedback

If a Feature is rejected, feedback is mandatory.

The system cannot regenerate a rejected Feature without human feedback.

---

## Approved Features Are Locked

Approved Features must remain unchanged during regeneration.

The system must not regenerate approved Features unless a future milestone explicitly supports reopening approval.

---

## Rejected Features Are Regenerated Individually

Only rejected Features are regenerated.

The rest of the Feature Set remains unchanged.

---

# 5. Human Review Actions

## Approve Feature

When the Product Manager approves a Feature:

* Feature status becomes Approved
* Feature is locked
* No feedback is required
* Feature remains part of the Feature Set
* Feature is not regenerated

---

## Reject Feature

When the Product Manager rejects a Feature:

* Feature status becomes Rejected
* Feedback is required
* Feature becomes eligible for regeneration
* Regeneration uses:

  * Original Epic
  * Current Feature
  * AI evaluation findings
  * Human rejection feedback
  * Existing approved Features for context

---

# 6. Regeneration Rules

## Rule 1 - Regenerate Only Rejected Features

The system must not regenerate the full Feature Set.

Only Features marked as Rejected are regenerated.

---

## Rule 2 - Preserve Approved Features

Approved Features remain unchanged.

They should be passed as context to the regeneration process so the new Feature avoids overlap.

---

## Rule 3 - Use Human Feedback as Primary Guidance

Human rejection feedback is the most important regeneration input.

AI evaluation findings provide supporting context.

---

## Rule 4 - Maintain Feature Identity

The regenerated Feature must have its own distinct business identity.

It should not duplicate an approved Feature.

It should not be a supporting activity inside another Feature.

---

## Rule 5 - Avoid Filler Features

The regenerated Feature should not exist only to preserve a fixed Feature count.

If the rejected Feature should be removed or merged conceptually, the regeneration output should explain that in its findings.

For Milestone 3, the system should still return a replacement Feature because full Feature removal is not yet implemented.

---

# 7. Regeneration Input Model

The regeneration service receives:

```json
{
  "epic": {
    "title": "",
    "description": "",
    "business_context": "",
    "success_metrics": ""
  },
  "rejected_feature": {
    "name": "",
    "description": "",
    "business_value": "",
    "acceptance_criteria": []
  },
  "ai_evaluation_findings": [],
  "human_rejection_feedback": "",
  "approved_features": [
    {
      "name": "",
      "description": "",
      "business_value": "",
      "acceptance_criteria": []
    }
  ]
}
```

---

# 8. Regeneration Output Model

The regeneration service returns one revised Feature.

```json
{
  "revised_feature": {
    "name": "",
    "description": "",
    "business_value": "",
    "acceptance_criteria": []
  },
  "revision_summary": [
    ""
  ]
}
```

The revised Feature is then evaluated again using the Milestone 2 Feature Evaluation workflow.

---

# 9. Workflow

```text
Epic
↓
Feature Set Generation
↓
Feature Set Evaluation
↓
Display Features + Evaluation Findings
↓
Human Feature Review
├── Approve Feature
│   ↓
│   Lock Feature
│
└── Reject Feature
    ↓
    Require Feedback
    ↓
    Regenerate Rejected Feature
    ↓
    Re-evaluate Revised Feature
    ↓
    Display Revised Feature
    ↓
    Human Review Again
```

---

# 10. LangGraph Flow

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

## Milestone 3

```text
Epic Intake
↓
Feature Generation
↓
Feature Evaluation
↓
Human Review
↓
Feature Regeneration
↓
Feature Evaluation
↓
Human Review
```

---

# 11. User Interface

For each Feature, display:

* Feature Name
* Description
* Business Value
* Acceptance Criteria
* AI Evaluation Recommendation
* AI Evaluation Findings
* Current Review Status
* Feature Version

## Human Actions

Each Feature should support:

* Approve
* Reject

## Reject Feedback

If the user selects Reject:

* Feedback textbox is required
* Regenerate button is enabled only after feedback is entered

## Approved Feature Display

Approved Features should visually indicate:

```text
Approved
Locked
```

## Rejected Feature Display

Rejected Features should visually indicate:

```text
Rejected
Feedback Required
Ready for Regeneration
```

## Regenerated Feature Display

Regenerated Features should show:

* Updated Feature content
* Revision summary
* New AI evaluation recommendation
* New AI evaluation findings
* Incremented version number

---

# 12. Review Status Values

A Feature can have one of the following statuses:

| Status         | Description                                     |
| -------------- | ----------------------------------------------- |
| Pending Review | Feature has not yet been reviewed by human      |
| Approved       | Feature has been approved and locked            |
| Rejected       | Feature has been rejected and requires feedback |
| Regenerated    | Feature has been revised after rejection        |

---

# 13. Version Management

Each Feature should maintain a version number.

Initial generated Features start at:

```text
v1
```

When a rejected Feature is regenerated:

```text
v1 → Rejected
v2 → Pending Review
```

If the regenerated Feature is rejected again:

```text
v2 → Rejected
v3 → Pending Review
```

Approved Features retain their approved version.

Example:

```text
Feature 1 v1 → Approved

Feature 2 v1 → Approved

Feature 3 v1 → Rejected
Feature 3 v2 → Pending Review
Feature 3 v2 → Approved
```

---

# 14. Expected Implementation Artifacts

## New Files

```text
src/
│
├── graph/
│   └── regeneration_node.py
│
├── models/
│   ├── feature_review.py
│   └── regeneration_result.py
│
├── prompts/
│   └── feature_regeneration.py
│
├── services/
│   └── feature_regeneration_service.py
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
├── models/
│   ├── feature.py
│   └── feature_set.py

src/
│
└── state/
    └── workflow_state.py
```

---

# 15. Repository Structure After Milestone 3

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
│   │   ├── evaluation_node.py
│   │   └── regeneration_node.py
│   │
│   ├── models/
│   │   ├── epic.py
│   │   ├── feature.py
│   │   ├── feature_set.py
│   │   ├── feature_evaluation.py
│   │   ├── evaluation_result.py
│   │   ├── feature_review.py
│   │   └── regeneration_result.py
│   │
│   ├── prompts/
│   │   ├── feature_generator.py
│   │   ├── feature_evaluation.py
│   │   └── feature_regeneration.py
│   │
│   ├── services/
│   │   ├── llm_service.py
│   │   ├── feature_evaluation_service.py
│   │   └── feature_regeneration_service.py
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

# 16. Prompt Requirements

Milestone 3 requires a new prompt document:

```text
docs/prompts/feature-regeneration-prompt.md
```

The code should load this prompt through:

```text
src/prompts/feature_regeneration.py
```

The prompt must instruct the model to:

* Regenerate only the rejected Feature
* Use human rejection feedback as primary guidance
* Use AI evaluation findings as supporting context
* Avoid overlap with approved Features
* Preserve business-user-facing capability orientation
* Avoid technical implementation details
* Maintain Feature identity
* Return exactly one revised Feature

---

# 17. Acceptance Criteria

## Functional

* User can approve individual Features
* User can reject individual Features
* Rejected Features require feedback
* Approved Features remain unchanged
* Only rejected Features are regenerated
* Regenerated Features receive a new version number
* Regenerated Features are evaluated again
* Regenerated Features can be reviewed again

## User Experience

* Review status is visible for each Feature
* Approved Features are clearly marked
* Rejected Features clearly require feedback
* Regeneration action is easy to understand
* Revised Features are displayed clearly
* Product Manager can focus only on Features needing attention

## Technical

* Existing Milestone 1 generation workflow remains intact
* Existing Milestone 2 evaluation workflow remains intact
* No ChromaDB integration is introduced
* No Confluence integration is introduced
* No persistent database is introduced
* Environment secrets are not committed

---

# 18. Explicitly Out of Scope

Do NOT implement:

* ChromaDB Integration
* Confluence Publishing
* Multi-user Approval
* Multi-reviewer Workflow
* Role-Based Permissions
* Persistent Database Storage
* User Story Generation
* Backlog Item Generation

These capabilities belong to future milestones.

---

# 19. Future Integration

## Milestone 4

Will store:

* Approved Features
* Rejected Features
* Human Rejection Feedback
* AI Evaluation Findings
* Feature Versions
* Regeneration History

## Milestone 5

Will publish:

* Approved Feature Set
* Approval Metadata
* Version History
* Evaluation Summary