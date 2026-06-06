from typing import Literal

from pydantic import BaseModel, Field


class FeatureEvaluation(BaseModel):
    feature_name: str = Field(..., min_length=1)
    recommendation: Literal["APPROVE", "REVIEW"]
    findings: list[str] = Field(..., min_length=1)
