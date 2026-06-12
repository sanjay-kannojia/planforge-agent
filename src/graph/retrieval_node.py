from src.models.retrieval_context import RetrievalContext
from src.services.learning_repository_service import LearningRepositoryService
from src.state.workflow_state import WorkflowState


def learning_retrieval_node(state: WorkflowState) -> dict:
    service = LearningRepositoryService()
    return {
        "learning_context": service.retrieve_similar_artifacts(state["epic"]),
    }


def rejected_lesson_retrieval_node(state: WorkflowState) -> dict:
    feature_set = state.get("feature_set")
    feature_reviews = state.get("feature_reviews")

    if feature_set is None:
        raise ValueError("Rejected lesson retrieval requires a FeatureSet.")
    if feature_reviews is None:
        raise ValueError("Rejected lesson retrieval requires human review decisions.")

    service = LearningRepositoryService()
    combined_context = RetrievalContext()
    for review in feature_reviews:
        if review.status != "Rejected" or not review.feedback.strip():
            continue

        rejected_feature = feature_set.features[review.feature_index]
        lesson_context = service.retrieve_rejected_lessons(
            epic=state["epic"],
            rejected_feature=rejected_feature,
            human_rejection_feedback=review.feedback,
        )
        combined_context.rejected_lessons.extend(lesson_context.rejected_lessons)

    return {"regeneration_learning_context": combined_context}
