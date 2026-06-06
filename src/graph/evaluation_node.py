from src.services.feature_evaluation_service import FeatureEvaluationService
from src.state.workflow_state import WorkflowState


def feature_evaluation_node(state: WorkflowState) -> dict:
    feature_set = state.get("feature_set")
    if feature_set is None:
        raise ValueError("Feature evaluation requires a generated FeatureSet.")

    service = FeatureEvaluationService()
    evaluation_result = service.evaluate_features(
        epic=state["epic"],
        feature_set=feature_set,
    )
    return {"evaluation_result": evaluation_result}
