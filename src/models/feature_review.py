from typing import Literal

from pydantic import BaseModel, Field


ReviewStatus = Literal["Pending Review", "Approved", "Rejected", "Regenerated"]


class FeatureReview(BaseModel):
    feature_index: int = Field(..., ge=0)
    status: ReviewStatus = "Pending Review"
    feedback: str = ""
    locked: bool = False
