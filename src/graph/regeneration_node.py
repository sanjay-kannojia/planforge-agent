from src.models.evaluation_result import EvaluationResult
from src.models.feature_review import FeatureReview
from src.models.feature_set import FeatureSet
from src.services.feature_regeneration_service import FeatureRegenerationService
from src.state.workflow_state import WorkflowState


def feature_regeneration_node(state: WorkflowState) -> dict:
    feature_set = state.get("feature_set")
    evaluation_result = state.get("evaluation_result")
    feature_reviews = state.get("feature_reviews")

    if feature_set is None:
        raise ValueError("Feature regeneration requires a FeatureSet.")
    if evaluation_result is None:
        raise ValueError("Feature regeneration requires AI evaluation results.")
    if feature_reviews is None:
        raise ValueError("Feature regeneration requires human review decisions.")

    updated_feature_set = feature_set.model_copy(deep=True)
    updated_reviews = [review.model_copy(deep=True) for review in feature_reviews]
    review_history = [entry.model_copy(deep=True) for entry in state.get("review_history") or []]
    evaluations_by_name = _evaluations_by_name(evaluation_result)
    service = FeatureRegenerationService()

    for review in updated_reviews:
        if review.status != "Rejected":
            continue

        if not review.feedback.strip():
            raise ValueError("Rejected Features require feedback before regeneration.")

        rejected_feature = updated_feature_set.features[review.feature_index]
        approved_features = _approved_features(updated_feature_set, updated_reviews)
        evaluation = evaluations_by_name.get(rejected_feature.name)
        ai_findings = evaluation.findings if evaluation else []

        regeneration_result = service.regenerate_feature(
            epic=state["epic"],
            rejected_feature=rejected_feature,
            ai_evaluation_findings=ai_findings,
            human_rejection_feedback=review.feedback,
            approved_features=approved_features,
            prior_rejection_attempts=_prior_rejection_attempts(
                review.feature_index,
                review_history,
            ),
            learning_context=state.get("regeneration_learning_context"),
        )
        revised_feature = regeneration_result.revised_feature
        revised_feature.version = rejected_feature.version + 1
        revised_feature.revision_summary = regeneration_result.revision_summary
        updated_feature_set.features[review.feature_index] = revised_feature
        review_history.append(
            _history_entry_for_regenerated_feature(
                feature_index=review.feature_index,
                feature=revised_feature,
            )
        )
        review.status = "Regenerated"
        review.feedback = ""
        review.locked = False

    return {
        "feature_set": updated_feature_set,
        "feature_reviews": updated_reviews,
        "review_history": review_history,
    }


def _evaluations_by_name(evaluation_result: EvaluationResult):
    return {evaluation.feature_name: evaluation for evaluation in evaluation_result.evaluations}


def _approved_features(feature_set: FeatureSet, feature_reviews: list[FeatureReview]):
    return [
        feature_set.features[review.feature_index]
        for review in feature_reviews
        if review.status == "Approved"
    ]


def _prior_rejection_attempts(feature_index: int, review_history):
    return [
        entry
        for entry in review_history
        if entry.feature_index == feature_index and entry.status == "Rejected"
    ]


def _history_entry_for_regenerated_feature(feature_index: int, feature):
    from src.models.learning_artifact import FeatureReviewHistoryEntry

    return FeatureReviewHistoryEntry(
        feature_index=feature_index,
        feature_name=feature.name,
        feature_version=feature.version,
        status="Regenerated",
        revision_summary=feature.revision_summary,
        feature_snapshot=feature.model_copy(deep=True),
    )
