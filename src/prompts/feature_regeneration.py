from functools import lru_cache
from pathlib import Path

from src.models.epic import Epic
from src.models.feature import Feature


PROMPT_PATH = Path(__file__).resolve().parents[2] / "docs" / "prompts" / "feature-regeneration-prompt.md"


@lru_cache
def load_feature_regeneration_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def build_feature_regeneration_prompt(
    epic: Epic,
    rejected_feature: Feature,
    ai_evaluation_findings: list[str],
    human_rejection_feedback: str,
    approved_features: list[Feature],
) -> str:
    prompt = load_feature_regeneration_prompt()
    approved_feature_context = (
        "\n\n".join(
            _format_feature_for_regeneration(index=index, feature=feature)
            for index, feature in enumerate(approved_features, start=1)
        )
        or "None"
    )
    evaluation_findings = "\n".join(f"- {finding}" for finding in ai_evaluation_findings) or "- None"
    rejected_acceptance_criteria = "\n".join(
        f"- {criterion}" for criterion in rejected_feature.acceptance_criteria
    )

    return f"""{prompt}

---

Regeneration Input

Epic

Title: {epic.title}
Description: {epic.description}
Business Context: {epic.business_context}
Success Metrics: {epic.success_metrics}

Rejected Feature

Name: {rejected_feature.name}
Description: {rejected_feature.description}
Business Value: {rejected_feature.business_value}
Acceptance Criteria:
{rejected_acceptance_criteria}

AI Evaluation Findings
{evaluation_findings}

Human Rejection Feedback
{human_rejection_feedback}

Approved Features To Preserve
{approved_feature_context}
"""


def _format_feature_for_regeneration(index: int, feature: Feature) -> str:
    acceptance_criteria = "\n".join(f"- {criterion}" for criterion in feature.acceptance_criteria)
    return f"""Approved Feature {index}
Name: {feature.name}
Description: {feature.description}
Business Value: {feature.business_value}
Acceptance Criteria:
{acceptance_criteria}"""
