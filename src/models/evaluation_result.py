from pydantic import BaseModel, Field

from src.models.feature_evaluation import FeatureEvaluation


class EvaluationResult(BaseModel):
    evaluations: list[FeatureEvaluation] = Field(..., min_length=1)
