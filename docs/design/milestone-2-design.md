# PlanForge

# Milestone 2 Design Document

## Phase 1: Epic to Feature Decomposition

## Milestone 2: Feature Evaluation and Approval Recommendation

---

# Document Status

Version 2.0

---

# 1. Objective

Milestone 2 introduces AI-based Feature Evaluation.

The goal is to reduce Product Manager review effort by evaluating generated Features and recommending whether they are likely to be approved.

The system does not replace Product Manager judgment.

The system acts as an experienced Product Management reviewer and provides recommendations before human review.

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
* Generate review findings
* Generate rejection reasons
* Generate regeneration guidance
* Display evaluation results

## Out of Scope

* Human approval workflow
* Feature regeneration
* ChromaDB integration
* Confluence publishing
* User Story generation

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

Question:

Does the Feature create meaningful business value?

Examples:

Good:

* Reduce staffing effort
* Improve compliance
* Increase forecasting accuracy

Weak:

* Administrative activity with unclear value
* Technical capability without measurable outcome

Priority:

Highest

---

## 5.2 Outcome Alignment

Question:

Does the Feature directly contribute to achieving the Epic objective?

Examples:

Epic:

AI-Powered Resource Matching

Good:

Intelligent Resource Matching

Weak:

User Theme Configuration

Priority:

High

---

## 5.3 Business Capability

Question:

Does the Feature represent a customer-facing or business-user-facing capability?

Examples:

Good:

* Resource Discovery
* Security Compliance Monitoring
* Forecast Approval and Review

Weak:

* Resource Database
* Forecast Engine
* Authentication API

Priority:

High

---

## 5.4 Scope Appropriateness

Question:

Is the Feature appropriately sized?

The Feature should not represent:

* An Epic
* A User Story
* A Technical Task

Priority:

Medium

---

## 5.5 Feature Uniqueness

Question:

Does the Feature significantly overlap with another generated Feature?

Priority:

Medium

---

# 6. Evaluation Output

The evaluator generates:

* Recommendation
* Findings
* Improvement Opportunities
* Regeneration Guidance

The evaluator may calculate internal scoring to support consistency.

Internal scores are not displayed to users.

---

# 7. Recommendation Types

## APPROVE

Feature is likely acceptable for Product Manager review and approval.

Characteristics:

* Strong business value
* Clear Epic alignment
* Appropriate scope
* Minimal overlap

---

## REVIEW

Feature may require Product Manager attention.

Characteristics:

* Moderate concerns
* Potential overlap
* Scope uncertainty
* Business value needs clarification

---

## REJECT

Feature is unlikely to be approved.

Characteristics:

* Weak business value
* Poor Epic alignment
* Technical implementation focus
* Significant overlap

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
  ],
  "improvement_opportunities": [],
  "regeneration_guidance": []
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
  ],
  "improvement_opportunities": [
    "Focus on staffing outcomes.",
    "Increase customer-facing value."
  ],
  "regeneration_guidance": [
    "Consider Resource Discovery.",
    "Consider Staffing Recommendation Review."
  ]
}
```

---

# 9. Workflow

Epic
↓
Feature Generation
↓
Feature Evaluation
↓
Approval Recommendation
↓
Display Results

---

# 10. LangGraph Flow

Milestone 1

Epic Intake
↓
Feature Generation
↓
Display Results

Milestone 2

Epic Intake
↓
Feature Generation
↓
Feature Evaluation
↓
Display Results

---

# 11. User Interface

For each generated Feature display:

Feature Name

AI Recommendation

Key Findings

Improvement Opportunities

Regeneration Guidance

Example:

Feature: Resource Discovery

Recommendation:

APPROVE

Findings:

* Strong business-user-facing capability
* Directly supports staffing outcomes
* Delivers measurable business value

Example:

Feature: Resource Profile Management

Recommendation:

REVIEW

Findings:

* Appears to be a supporting capability
* Business value is indirect

Improvement Opportunities:

* Focus on staffing outcomes
* Increase customer-facing value

---

# 12. Human Interaction Model

The Product Manager is not expected to score Features.

The Product Manager performs one of two actions:

## Approve

No feedback required.

Stored:

* Feature
* AI Recommendation
* Approved Status

---

## Reject

Feedback is mandatory.

Examples:

* Business value unclear
* Too broad
* Too technical
* Missing customer impact
* Overlaps another Feature

Stored:

* Feature
* AI Recommendation
* Rejection Feedback

---

# 13. Benchmark Evaluation

Evaluation decisions should be informed by approved decomposition examples stored under:

sample_epics/

These examples represent approved Product Manager decompositions and serve as reference patterns for quality evaluation.

---

# 14. Acceptance Criteria

## Functional

* Evaluate every generated Feature
* Produce approval recommendation
* Generate findings
* Generate improvement opportunities
* Generate regeneration guidance

## User Experience

* Recommendations visible in Streamlit
* Findings easy to understand
* Weak Features easy to identify
* Human approval effort reduced

---

# 15. Future Integration

## Milestone 3

Consumes:

* Recommendation
* Findings
* Regeneration Guidance
* Human Rejection Feedback

---

## Milestone 4

Stores:

* Approved Features
* Rejected Features
* AI Recommendations
* Human Feedback
* Regeneration History

---

## Milestone 5

Publishes:

* Approved Features
* Approval Metadata
* Evaluation Summary