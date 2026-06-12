from functools import lru_cache
from pathlib import Path


from src.models.epic import Epic
from src.models.retrieval_context import RetrievalContext
from src.prompts.retrieval_context import format_retrieval_context_for_generation


PROMPT_PATH = Path(__file__).resolve().parents[2] / "docs" / "prompts" / "feature-generation-prompt.md"


@lru_cache
def load_feature_generation_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def build_feature_generation_prompt(
    epic: Epic,
    learning_context: RetrievalContext | None = None,
) -> str:
    prompt = load_feature_generation_prompt()
    return f"""{prompt}

---

Retrieved Organizational Learning Context

Use this context as guidance for decomposition patterns and lessons learned.
Do not copy prior Feature names unless they naturally fit the current Epic.
The current Epic remains the source of truth.

{format_retrieval_context_for_generation(learning_context)}

---

Epic Input

Title: {epic.title}
Description: {epic.description}
Business Context: {epic.business_context}
Success Metrics: {epic.success_metrics}
"""
