# PlanForge

# Milestone 4 Design Document

## Phase 1: Epic to Feature Decomposition

## Milestone 4: Organizational Learning Repository and Retrieval

---

# Document Status

Version 1.0

---

# 1. Objective

Milestone 4 introduces organizational learning using ChromaDB.

The goal is to store completed, reviewed Epic-to-Feature decompositions and retrieve similar approved decomposition patterns when generating Features for a new Epic.

PlanForge should learn from prior Product Manager-approved outcomes and use those patterns to improve future Feature generation and regeneration.

---

# 2. Business Problem

Feature generation improves when the agent can learn from prior approved decomposition patterns.

Without organizational learning, every Epic is processed as if PlanForge has no historical memory.

This creates problems:

* The agent may repeat prior mistakes.
* The agent may miss common decomposition patterns.
* The agent cannot reuse approved planning knowledge.
* Product Manager feedback does not improve future outputs.
* Rejected Feature lessons are not available for future regeneration patterns.

Milestone 4 allows PlanForge to retain and retrieve organizational planning knowledge after reviewed decompositions are completed.

---

# 3. Core Design Decision

PlanForge separates active workflow memory from organizational learning.

## Active Workflow Memory

Used during the current user session.

Managed by:

* LangGraph state
* Streamlit session state

Stores:

* Current Epic
* Current Feature Set
* Approved Features
* Rejected Features
* Human rejection feedback
* Regenerated Feature versions
* AI evaluation findings

Purpose:

Support the current review and regeneration cycle.

---

## Organizational Learning Repository

Used across future Epic decomposition sessions.

Managed by:

* ChromaDB

Stores:

* Completed approved Epic Decomposition Artifacts
* Final approved Feature Sets
* Rejected Feature lessons from completed sessions
* Human rejection feedback
* AI evaluation findings
* Version and regeneration history summaries

Purpose:

Improve future Feature generation and regeneration by retrieving similar approved decomposition patterns and prior rejection lessons.

---

# 4. Primary Learning Unit

The primary learning unit is an Epic Decomposition Artifact.

PlanForge should retrieve similar Epic-to-Feature decomposition artifacts, not isolated Features.

A Feature only makes sense within the Epic it supports.

For example:

```text
Security Compliance Monitoring
```

is a strong Feature for:

```text
Enable Service Health Security Compliance
```

but may not be useful for:

```text
AI-Powered Resource Matching
```

Therefore, the primary learning artifact is:

```text
Epic
+
Final Approved Feature Set
+
Rejected Feature Lessons
+
Human Feedback
+
Version History Summary
```

not an individual Feature alone.

---

# 5. Scope

## In Scope

* Store completed approved Epic Decomposition Artifacts
* Store final approved Feature Sets
* Store rejected Features from completed review sessions
* Store human rejection feedback
* Store AI evaluation findings
* Store Feature version history summary
* Store regeneration history summary
* Retrieve similar approved Epic Decomposition Artifacts before Feature generation
* Use retrieved decomposition patterns as context for generation
* Retrieve relevant rejection lessons during Feature regeneration
* Display retrieved learning context summary in the UI

---

## Out of Scope

* Confluence publishing
* Persistent relational database
* Full audit-grade workflow history
* Multi-user learning repository
* Role-based access control
* Enterprise authentication
* Enterprise search
* Automated approval decisions
* User Story generation
* Backlog Item generation

---

# 6. Storage Timing

PlanForge stores learning artifacts in ChromaDB only after the complete Feature Set reaches an approved state.

A complete approved state means:

* Every Feature in the Feature Set has been approved by the Product Manager.
* Rejected Features, if any, have been regenerated and eventually approved or replaced.
* The review cycle for the Epic is complete.

PlanForge does not store every intermediate draft as an independent organizational learning artifact.

Reason:

Intermediate drafts may contain incomplete, low-quality, or unresolved work. Storing every intermediate draft directly in ChromaDB would create noisy retrieval results.

---

# 7. Active Review History

During the active review cycle, PlanForge must retain every Feature decision in workflow state.

This includes:

* Approved Features
* Rejected Features
* Human rejection feedback
* AI evaluation findings
* Regenerated versions
* Revision summaries
* Current Feature statuses

This active review history is used immediately for targeted regeneration.

Example:

```text
Feature 1 v1 → Approved

Feature 2 v1 → Rejected
Feedback: Business value unclear

Feature 3 v1 → Rejected
Feedback: Too broad
```

PlanForge must remember Feature 2 and Feature 3 feedback during the current session so it can regenerate those Features.

If Feature 2 is approved after regeneration but Feature 3 is rejected again:

```text
Feature 2 v2 → Approved

Feature 3 v2 → Rejected
Feedback: Still overlaps with Feature 1
```

PlanForge must use both Feature 3 rejection attempts and feedback when regenerating Feature 3 again.

This active review history belongs in workflow state, not ChromaDB.

---

# 8. Organizational Learning Storage

After the full Feature Set reaches approval, PlanForge persists the completed reviewed session into ChromaDB.

The stored artifact includes:

* Original Epic
* Final approved Feature Set
* Approved Features
* Rejected Feature attempts from the session
* Human rejection feedback
* AI evaluation findings
* Feature version history summary
* Regeneration history summary
* Metadata

This gives the learning repository both:

```text
Approved final decomposition pattern
+
Rejected lessons that explain what was improved
```

---

# 9. Storage Model

## 9.1 Epic Decomposition Artifact

The primary storage unit is an Epic Decomposition Artifact.

```json
{
  "artifact_type": "epic_decomposition",
  "epic": {
    "title": "",
    "description": "",
    "business_context": "",
    "success_metrics": ""
  },
  "final_approved_features": [
    {
      "name": "",
      "description": "",
      "business_value": "",
      "acceptance_criteria": [],
      "approved_version": ""
    }
  ],
  "rejected_feature_lessons": [
    {
      "original_feature_name": "",
      "rejected_version": "",
      "description": "",
      "business_value": "",
      "human_feedback": "",
      "ai_findings": [],
      "replacement_feature_name": "",
      "final_resolution": ""
    }
  ],
  "ai_evaluations": [
    {
      "feature_name": "",
      "recommendation": "",
      "findings": []
    }
  ],
  "version_history_summary": [
    {
      "feature_name": "",
      "versions": [],
      "final_status": ""
    }
  ],
  "metadata": {
    "domain": "",
    "status": "approved",
    "created_at": "",
    "source": "PlanForge"
  }
}
```

---

## 9.2 Final Approved Feature Set

The final approved Feature Set is stored as part of the Epic Decomposition Artifact.

Purpose:

* Preserve approved decomposition patterns
* Provide examples for similar future Epics
* Improve generation quality
* Help the agent understand how successful Epics were decomposed

---

## 9.3 Rejected Feature Lessons

Rejected Features are stored only as part of a completed approved decomposition session.

A rejected Feature lesson must include:

* Rejected Feature content
* Human rejection feedback
* AI evaluation findings
* Version number
* Replacement Feature reference, if available
* Final resolution

Purpose:

* Preserve what did not work
* Avoid repeated mistakes
* Improve future regeneration
* Show how human feedback improved the final approved Feature Set

Rejected Features should never be retrieved without their human feedback.

A rejected Feature without feedback has limited learning value.

---

# 10. Retrieval Strategy

## 10.1 Initial Feature Generation

For a new Epic, PlanForge retrieves similar approved Epic Decomposition Artifacts.

Retrieval input:

```text
Epic Title
Epic Description
Business Context
Success Metrics
```

Retrieval output:

```text
Similar Approved Epics
Final Approved Feature Sets
Decomposition Patterns
Rejected Lessons, if relevant
```

The retrieved context is passed into Feature generation.

The generation prompt should use retrieved artifacts as guidance, not as content to copy.

---

## 10.2 Feature Regeneration

When a Feature is rejected, PlanForge uses two context sources.

### Current Session Context

From workflow state:

* Current Epic
* Approved Features in current session
* Rejected Feature
* Human rejection feedback
* Previous rejection attempts for that Feature
* AI evaluation findings

### Organizational Learning Context

From ChromaDB:

* Similar approved Epic Decomposition Artifacts
* Relevant rejected Feature lessons with feedback

The regeneration prompt should prioritize:

1. Human rejection feedback from the current session
2. Current Epic objective
3. Approved Features from the current session
4. Prior rejection attempts for the same Feature
5. Retrieved organizational learning context
6. AI evaluation findings

---

# 11. Retrieval Principles

## Principle 1

Retrieve decomposition patterns, not isolated Feature names.

---

## Principle 2

Approved artifacts guide generation.

---

## Principle 3

Rejected lessons guide avoidance.

---

## Principle 4

Human feedback is more important than AI findings.

---

## Principle 5

Current Epic context remains the source of truth.

Retrieved artifacts are guidance only.

---

## Principle 6

Current session feedback has priority over historical feedback.

---

# 12. Generation With Retrieved Context

Feature generation should receive:

* New Epic
* Similar approved Epic summaries
* Final approved Feature Set patterns
* Relevant rejected lessons, if available

The model should use retrieved examples to understand decomposition patterns.

It should not copy prior Feature names unless they naturally fit the new Epic.

Example retrieved pattern:

```text
Governance Epic
↓
Compliance Monitoring
Authentication Security
Regional Privacy Compliance
```

New Epic:

```text
Improve cloud service compliance posture
```

Possible generated Features:

```text
Compliance Risk Monitoring
Access Control Review
Regional Regulatory Compliance
Security Remediation Tracking
```

---

# 13. Regeneration With Retrieved Context

Feature regeneration should receive:

* Rejected Feature
* Human rejection feedback
* Current approved Features
* Prior rejection attempts for the same Feature
* Similar approved decomposition patterns
* Relevant rejected lessons from prior completed sessions

The regenerated Feature must:

* Address current human feedback
* Avoid overlap with approved Features
* Avoid repeating prior rejected patterns
* Maintain its own business identity
* Deliver meaningful business value

---

# 14. User Interface

The UI should show a simple learning context summary.

Example:

```text
Retrieved Learning Context

2 similar approved decomposition artifacts found.

Similar Epic:
Enable Service Health Security Compliance

Pattern:
- Compliance Monitoring
- Authentication Security
- Regional Privacy Compliance
```

The UI should not expose raw ChromaDB results.

The Product Manager should see enough to understand that PlanForge used prior learning, without being overwhelmed by retrieval details.

---

# 15. ChromaDB Collections

## Collection 1

```text
epic_decompositions
```

Stores completed approved Epic Decomposition Artifacts.

Used for:

* Similar Epic retrieval
* Feature generation context
* Approved decomposition pattern reuse

---

## Collection 2

```text
rejected_feature_lessons
```

Stores rejected Feature lessons extracted from completed approved Epic Decomposition Artifacts.

Used for:

* Regeneration guidance
* Avoiding repeated mistakes
* Learning from human feedback

Rejected lessons must include human feedback.

---

# 16. Metadata

Each stored artifact should include metadata.

Recommended metadata:

```json
{
  "artifact_type": "epic_decomposition",
  "status": "approved",
  "domain": "",
  "created_at": "",
  "feature_count": 0,
  "source": "PlanForge"
}
```

Metadata helps filter retrieval results.

---

# 17. Workflow

## Current Milestone 3 Workflow

```text
Epic
↓
Feature Set Generation
↓
Feature Set Evaluation
↓
Human Review
↓
Targeted Regeneration
```

## Milestone 4 Workflow

```text
Epic
↓
Retrieve Similar Epic Decomposition Artifacts
↓
Feature Set Generation with Retrieved Context
↓
Feature Set Evaluation
↓
Human Review
↓
Targeted Regeneration with Current Session + Retrieved Context
↓
Store Completed Approved Decomposition Artifact
```

---

# 18. LangGraph Flow

```text
Epic Intake
↓
Learning Retrieval
↓
Feature Generation
↓
Feature Evaluation
↓
Human Review
↓
Feature Regeneration
↓
Learning Store
```

Learning Store executes only after the full Feature Set is approved.

---

# 19. Expected Implementation Artifacts

## New Files

```text
src/
│
├── graph/
│   ├── retrieval_node.py
│   └── learning_store_node.py
│
├── models/
│   ├── learning_artifact.py
│   └── retrieval_context.py
│
├── services/
│   └── learning_repository_service.py
│
├── prompts/
│   └── retrieval_context.py
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
├── services/
│   ├── llm_service.py
│   └── feature_regeneration_service.py

src/
│
└── state/
    └── workflow_state.py

requirements.txt
.env.example
```

---

# 20. Repository Structure After Milestone 4

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
│   │   ├── regeneration_node.py
│   │   ├── retrieval_node.py
│   │   └── learning_store_node.py
│   │
│   ├── models/
│   │   ├── epic.py
│   │   ├── feature.py
│   │   ├── feature_set.py
│   │   ├── feature_evaluation.py
│   │   ├── evaluation_result.py
│   │   ├── feature_review.py
│   │   ├── regeneration_result.py
│   │   ├── learning_artifact.py
│   │   └── retrieval_context.py
│   │
│   ├── prompts/
│   │   ├── feature_generator.py
│   │   ├── feature_evaluation.py
│   │   ├── feature_regeneration.py
│   │   └── retrieval_context.py
│   │
│   ├── services/
│   │   ├── llm_service.py
│   │   ├── feature_evaluation_service.py
│   │   ├── feature_regeneration_service.py
│   │   └── learning_repository_service.py
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

# 21. Environment Variables

Add to `.env.example`:

```text
CHROMA_DB_PATH=./chroma_db
CHROMA_COLLECTION_EPIC_DECOMPOSITIONS=epic_decompositions
CHROMA_COLLECTION_REJECTED_FEATURE_LESSONS=rejected_feature_lessons
```

The real `.env` remains local and must not be committed.

---

# 22. Acceptance Criteria

## Functional

* Similar approved Epic Decomposition Artifacts are retrieved before generation
* Retrieved context is passed into Feature generation
* Rejected Feature lessons can be retrieved during regeneration
* Current session review history remains in workflow state
* Completed approved Feature Sets are stored as Epic Decomposition Artifacts
* Rejected Features and human feedback from the completed session are stored as learning lessons
* Learning Store executes only after the full Feature Set is approved
* Intermediate draft states are not stored as standalone organizational learning artifacts
* ChromaDB stores artifacts locally
* Retrieved context is visible in the UI as a summary

## Product Quality

* Retrieved examples improve decomposition pattern quality
* Retrieved context does not cause copied Features
* New Epic remains the primary source of truth
* Similarity retrieval focuses on Epic-level similarity
* Rejected lessons are retrieved with human feedback

## Technical

* ChromaDB is used as the semantic retrieval layer
* LangGraph/workflow state is used for active review history
* No Confluence publishing is introduced
* No persistent relational database is introduced
* Existing Milestone 1, 2, and 3 workflows remain intact
* Environment secrets are not committed

---

# 23. Explicitly Out of Scope

Do NOT implement:

* Confluence Publishing
* Persistent Relational Database
* Multi-user Learning Repository
* Enterprise Authentication
* User Story Generation
* Backlog Item Generation
* Automated Approval
* Role-Based Access Control

These capabilities belong to future milestones.

---

# 24. Future Integration

## Milestone 5

Will publish:

* Approved Feature Set
* Approval Metadata
* Evaluation Summary
* Learning Context Summary

## Future Persistence Layer

A future version may introduce a relational database for:

* Full workflow history
* Auditability
* Multi-user review
* Approval history
* Artifact version lineage

ChromaDB remains the semantic retrieval layer.