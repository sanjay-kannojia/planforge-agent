from pydantic import BaseModel, Field

from src.models.feature import Feature


class RegenerationResult(BaseModel):
    revised_feature: Feature
    revision_summary: list[str] = Field(..., min_length=1)
