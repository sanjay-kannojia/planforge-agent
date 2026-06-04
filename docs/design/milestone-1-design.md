# PlanForge

## Milestone 1 Technical Design

**Document Version:** 1.0

---

# 1. Objective

Milestone 1 demonstrates the core capability of PlanForge:

```text
Epic
  ↓
Feature Generation
  ↓
Feature Display
```

The objective is to validate that AI can generate business-oriented Features from an Epic using the Feature Generation Prompt.

This milestone intentionally excludes validation, review workflows, enterprise integrations, and organizational learning.

---

# 2. Scope

## Included

* Streamlit user interface
* Epic data capture
* LangGraph workflow
* OpenAI integration
* Feature generation prompt
* Pydantic models
* Feature display

---

## Excluded

* Feature validation
* Human review workflow
* Feature regeneration
* Confluence integration
* ChromaDB integration
* LangSmith tracing
* Authentication
* Persistence

---

# 3. User Flow

```text
User enters Epic
        ↓
Generate Features
        ↓
LangGraph executes workflow
        ↓
OpenAI generates Features
        ↓
Pydantic validates schema
        ↓
Features displayed in UI
```

---

# 4. Inputs

## Epic Title

Short title of the initiative.

Example:

```text
AI-Powered Resource Matching
```

---

## Epic Description

Business objective description.

Example:

```text
Provide intelligent recommendations for matching resources to projects.
```

---

## Business Context

Business problem being solved.

Example:

```text
Resource managers spend significant time manually identifying suitable resources.
```

---

## Success Metrics

Expected business outcomes.

Example:

```text
Reduce staffing effort by 30%.
Increase project fulfillment accuracy by 20%.
```

---

# 5. Outputs

## Feature Set

Each generated Feature must contain:

| Field               | Required |
| ------------------- | -------- |
| Name                | Yes      |
| Description         | Yes      |
| Business Value      | Yes      |
| Acceptance Criteria | Yes      |

---

# 6. Architecture

## Workflow

```text
Epic Intake
    ↓
Feature Generation
    ↓
Display Results
```

---

## LangGraph Nodes

### Node 1

Epic Intake

Responsibility:

Capture Epic information and create workflow state.

---

### Node 2

Feature Generation

Responsibility:

Invoke OpenAI using the Feature Generation Prompt.

Return Feature Set.

---

### Node 3

Display Results

Responsibility:

Render generated Features in Streamlit.

---

# 7. Pydantic Models

## Epic

```python
class Epic:
    title: str
    description: str
    business_context: str
    success_metrics: str
```

---

## Feature

```python
class Feature:
    name: str
    description: str
    business_value: str
    acceptance_criteria: list[str]
```

---

## FeatureSet

```python
class FeatureSet:
    features: list[Feature]
```

---

# 8. Workflow State

```python
class WorkflowState:
    epic: Epic
    feature_set: FeatureSet | None
```

---

# 9. Repository Structure

```text
planforge/
│
├── app.py
│
├── src/
│   ├── graph/
│   │   └── workflow.py
│   │
│   ├── models/
│   │   ├── epic.py
│   │   ├── feature.py
│   │   └── feature_set.py
│   │
│   ├── prompts/
│   │   └── feature_generator.py
│   │
│   ├── services/
│   │   └── llm_service.py
│   │
│   └── state/
│       └── workflow_state.py
│
├── tests/
│
└── requirements.txt
```

---

# 10. OpenAI Integration

The system shall:

1. Load the Feature Generation Prompt.
2. Inject Epic information.
3. Invoke the configured OpenAI model.
4. Parse JSON response.
5. Validate output using Pydantic.

---

# 11. Error Handling

The system shall handle:

* Empty Epic inputs
* Invalid JSON responses
* OpenAI API failures
* Schema validation failures

The user shall receive meaningful error messages.

---

# 12. Success Criteria

Milestone 1 is complete when:

* User can enter Epic information.
* LangGraph workflow executes successfully.
* OpenAI generates Features.
* Output conforms to schema.
* Features are displayed in Streamlit.
* Generated Features represent business capabilities rather than technical implementations.

---

# 13. Sample Test Scenario

## Epic

AI-Powered Resource Matching

### Description

Provide intelligent recommendations for matching resources to projects.

### Business Context

Resource managers currently perform staffing manually.

### Success Metrics

Reduce staffing effort by 30%.

---

## Expected Features

Examples:

* Resource Discovery and Search
* Intelligent Resource Matching
* Staffing Approval Workflow
* Resource Recommendation Transparency
* Staffing Performance Analytics

The exact output may vary, but generated Features should represent business capabilities rather than technical implementation tasks.