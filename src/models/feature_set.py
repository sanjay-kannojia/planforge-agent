from pydantic import BaseModel, Field

from src.models.feature import Feature


class FeatureSet(BaseModel):
    features: list[Feature] = Field(..., min_length=1)
