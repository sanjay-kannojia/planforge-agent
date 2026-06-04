from typing import Optional, TypedDict

from src.models.epic import Epic
from src.models.feature_set import FeatureSet


class WorkflowState(TypedDict):
    epic: Epic
    feature_set: Optional[FeatureSet]
