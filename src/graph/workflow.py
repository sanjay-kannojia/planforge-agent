from langgraph.graph import END, StateGraph

from src.graph.evaluation_node import feature_evaluation_node
from src.graph.learning_store_node import learning_store_node
from src.graph.regeneration_node import feature_regeneration_node
from src.graph.retrieval_node import learning_retrieval_node, rejected_lesson_retrieval_node
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
    feature_set = service.generate_features(
        epic=state["epic"],
        learning_context=state.get("learning_context"),
    )
    return {"feature_set": feature_set}


def build_workflow():
    graph = StateGraph(WorkflowState)

    graph.add_node("epic_intake", epic_intake_node)
    graph.add_node("learning_retrieval", learning_retrieval_node)
    graph.add_node("feature_generation", feature_generation_node)
    graph.add_node("feature_evaluation", feature_evaluation_node)

    graph.set_entry_point("epic_intake")
    graph.add_edge("epic_intake", "learning_retrieval")
    graph.add_edge("learning_retrieval", "feature_generation")
    graph.add_edge("feature_generation", "feature_evaluation")
    graph.add_edge("feature_evaluation", END)

    return graph.compile()


def build_regeneration_workflow():
    graph = StateGraph(WorkflowState)

    graph.add_node("rejected_lesson_retrieval", rejected_lesson_retrieval_node)
    graph.add_node("feature_regeneration", feature_regeneration_node)
    graph.add_node("feature_evaluation", feature_evaluation_node)

    graph.set_entry_point("rejected_lesson_retrieval")
    graph.add_edge("rejected_lesson_retrieval", "feature_regeneration")
    graph.add_edge("feature_regeneration", "feature_evaluation")
    graph.add_edge("feature_evaluation", END)

    return graph.compile()


def build_learning_store_workflow():
    graph = StateGraph(WorkflowState)

    graph.add_node("learning_store", learning_store_node)

    graph.set_entry_point("learning_store")
    graph.add_edge("learning_store", END)

    return graph.compile()


def run_workflow(epic: Epic) -> WorkflowState:
    app = build_workflow()
    return app.invoke(
        {
            "epic": epic,
            "feature_set": None,
            "evaluation_result": None,
            "feature_reviews": None,
            "review_history": None,
            "learning_context": None,
            "regeneration_learning_context": None,
            "stored_learning_artifact": None,
        }
    )


def run_regeneration_workflow(
    epic: Epic,
    feature_set: FeatureSet,
    evaluation_result: EvaluationResult,
    feature_reviews: list[FeatureReview],
    review_history: list | None = None,
) -> WorkflowState:
    app = build_regeneration_workflow()
    return app.invoke(
        {
            "epic": epic,
            "feature_set": feature_set,
            "evaluation_result": evaluation_result,
            "feature_reviews": feature_reviews,
            "review_history": review_history or [],
            "learning_context": None,
            "regeneration_learning_context": None,
            "stored_learning_artifact": None,
        }
    )


def store_learning_artifact(
    epic: Epic,
    feature_set: FeatureSet,
    evaluation_result: EvaluationResult,
    feature_reviews: list[FeatureReview],
    review_history: list | None = None,
) -> WorkflowState:
    app = build_learning_store_workflow()
    return app.invoke(
        {
            "epic": epic,
            "feature_set": feature_set,
            "evaluation_result": evaluation_result,
            "feature_reviews": feature_reviews,
            "review_history": review_history or [],
            "learning_context": None,
            "regeneration_learning_context": None,
            "stored_learning_artifact": None,
        }
    )
