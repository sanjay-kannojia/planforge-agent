from typing import Optional, TypedDict

from src.models.epic import Epic
from src.models.evaluation_result import EvaluationResult
from src.models.feature_review import FeatureReview
from src.models.feature_set import FeatureSet
from src.models.learning_artifact import EpicDecompositionArtifact, FeatureReviewHistoryEntry
from src.models.retrieval_context import RetrievalContext


class WorkflowState(TypedDict):
    epic: Epic
    feature_set: Optional[FeatureSet]
    evaluation_result: Optional[EvaluationResult]
    feature_reviews: Optional[list[FeatureReview]]
    review_history: Optional[list[FeatureReviewHistoryEntry]]
    learning_context: Optional[RetrievalContext]
    regeneration_learning_context: Optional[RetrievalContext]
    stored_learning_artifact: Optional[EpicDecompositionArtifact]
