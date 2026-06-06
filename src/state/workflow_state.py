from typing import Optional, TypedDict

from src.models.epic import Epic
from src.models.evaluation_result import EvaluationResult
from src.models.feature_set import FeatureSet


class WorkflowState(TypedDict):
    epic: Epic
    feature_set: Optional[FeatureSet]
    evaluation_result: Optional[EvaluationResult]
