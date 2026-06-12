from src.models.feature_review import FeatureReview
from src.services.learning_repository_service import LearningRepositoryService
from src.state.workflow_state import WorkflowState


def learning_store_node(state: WorkflowState) -> dict:
    feature_set = state.get("feature_set")
    evaluation_result = state.get("evaluation_result")
    feature_reviews = state.get("feature_reviews")
    review_history = state.get("review_history") or []

    if feature_set is None:
        raise ValueError("Learning storage requires a completed FeatureSet.")
    if evaluation_result is None:
        raise ValueError("Learning storage requires AI evaluation results.")
    if feature_reviews is None:
        raise ValueError("Learning storage requires human review decisions.")
    if not _all_features_approved(feature_reviews):
        raise ValueError("Learning artifacts can only be stored after all Features are approved.")

    service = LearningRepositoryService()
    artifact = service.store_completed_artifact(
        epic=state["epic"],
        feature_set=feature_set,
        evaluation_result=evaluation_result,
        review_history=review_history,
    )
    return {"stored_learning_artifact": artifact}


def _all_features_approved(feature_reviews: list[FeatureReview]) -> bool:
    return bool(feature_reviews) and all(review.status == "Approved" for review in feature_reviews)
