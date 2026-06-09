from langgraph.graph import END, StateGraph

from src.graph.evaluation_node import feature_evaluation_node
from src.graph.regeneration_node import feature_regeneration_node
from src.models.epic import Epic
from src.models.evaluation_result import EvaluationResult
from src.models.feature_review import FeatureReview
from src.models.feature_set import FeatureSet
from src.services.llm_service import OpenAIService
from src.state.workflow_state import WorkflowState


def epic_intake_node(state: WorkflowState) -> dict:
    return {"epic": state["epic"]}


def feature_generation_node(state: WorkflowState) -> dict:
    service = OpenAIService()
    feature_set = service.generate_features(state["epic"])
    return {"feature_set": feature_set}


def build_workflow():
    graph = StateGraph(WorkflowState)

    graph.add_node("epic_intake", epic_intake_node)
    graph.add_node("feature_generation", feature_generation_node)
    graph.add_node("feature_evaluation", feature_evaluation_node)

    graph.set_entry_point("epic_intake")
    graph.add_edge("epic_intake", "feature_generation")
    graph.add_edge("feature_generation", "feature_evaluation")
    graph.add_edge("feature_evaluation", END)

    return graph.compile()


def build_regeneration_workflow():
    graph = StateGraph(WorkflowState)

    graph.add_node("feature_regeneration", feature_regeneration_node)
    graph.add_node("feature_evaluation", feature_evaluation_node)

    graph.set_entry_point("feature_regeneration")
    graph.add_edge("feature_regeneration", "feature_evaluation")
    graph.add_edge("feature_evaluation", END)

    return graph.compile()


def run_workflow(epic: Epic) -> WorkflowState:
    app = build_workflow()
    return app.invoke(
        {
            "epic": epic,
            "feature_set": None,
            "evaluation_result": None,
            "feature_reviews": None,
        }
    )


def run_regeneration_workflow(
    epic: Epic,
    feature_set: FeatureSet,
    evaluation_result: EvaluationResult,
    feature_reviews: list[FeatureReview],
) -> WorkflowState:
    app = build_regeneration_workflow()
    return app.invoke(
        {
            "epic": epic,
            "feature_set": feature_set,
            "evaluation_result": evaluation_result,
            "feature_reviews": feature_reviews,
        }
    )
