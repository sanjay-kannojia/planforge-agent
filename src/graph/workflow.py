from langgraph.graph import END, StateGraph

from src.models.epic import Epic
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

    graph.set_entry_point("epic_intake")
    graph.add_edge("epic_intake", "feature_generation")
    graph.add_edge("feature_generation", END)

    return graph.compile()


def run_workflow(epic: Epic) -> WorkflowState:
    app = build_workflow()
    return app.invoke({"epic": epic, "feature_set": None})
