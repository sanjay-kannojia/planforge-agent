from functools import lru_cache
from pathlib import Path


from src.models.epic import Epic


PROMPT_PATH = Path(__file__).resolve().parents[2] / "docs" / "prompts" / "feature-generation-prompt.md"


@lru_cache
def load_feature_generation_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def build_feature_generation_prompt(epic: Epic) -> str:
    prompt = load_feature_generation_prompt()
    return f"""{prompt}

---

Epic Input

Title: {epic.title}
Description: {epic.description}
Business Context: {epic.business_context}
Success Metrics: {epic.success_metrics}
"""
