from functools import lru_cache
from pathlib import Path

from src.models.epic import Epic
from src.models.feature import Feature
from src.models.feature_set import FeatureSet


PROMPT_PATH = Path(__file__).resolve().parents[2] / "docs" / "prompts" / "feature-evaluation-prompt.md"


@lru_cache
def load_feature_evaluation_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def build_feature_set_evaluation_prompt(epic: Epic, feature_set: FeatureSet) -> str:
    prompt = load_feature_evaluation_prompt()
    features = "\n\n".join(
        _format_feature_for_evaluation(index=index, feature=feature)
        for index, feature in enumerate(feature_set.features, start=1)
    )

    return f"""{prompt}

---

Milestone 2 Output Requirements

Evaluate the entire Feature Set in one response.
Evaluate each generated Feature independently.
Return exactly one evaluation result per generated Feature.
Return valid JSON only using this exact shape:

{{
  "evaluations": [
    {{
      "feature_name": "",
      "recommendation": "APPROVE | REVIEW",
      "findings": [
        ""
      ]
    }}
  ]
}}

Use only APPROVE or REVIEW as the recommendation.
Generate concise findings that explain each recommendation.
Do not generate human approval actions, rejection workflow, regeneration guidance, Confluence content, ChromaDB content, or User Stories.

---

Epic Input

Title: {epic.title}
Description: {epic.description}
Business Context: {epic.business_context}
Success Metrics: {epic.success_metrics}

---

Generated Feature Set

{features}
"""


def _format_feature_for_evaluation(index: int, feature: Feature) -> str:
    acceptance_criteria = "\n".join(f"- {criterion}" for criterion in feature.acceptance_criteria)
    return f"""Feature {index}
Name: {feature.name}
Description: {feature.description}
Business Value: {feature.business_value}
Acceptance Criteria:
{acceptance_criteria}"""
