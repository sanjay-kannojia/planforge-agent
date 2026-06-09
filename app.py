import os

import streamlit as st
from dotenv import load_dotenv

from src.graph.workflow import run_regeneration_workflow, run_workflow
from src.models.epic import Epic
from src.models.feature_review import FeatureReview


load_dotenv()


st.set_page_config(page_title="PlanForge", layout="wide")

st.title("PlanForge")
st.caption("Epic to Feature generation")


def initialize_feature_reviews(feature_count: int) -> list[FeatureReview]:
    return [FeatureReview(feature_index=index) for index in range(feature_count)]


def reviews_by_index() -> dict[int, FeatureReview]:
    return {
        review.feature_index: review
        for review in st.session_state.get("feature_reviews", [])
    }


def set_review_status(index: int, status: str, feedback: str = "") -> None:
    reviews = st.session_state.get("feature_reviews", [])
    for review in reviews:
        if review.feature_index == index:
            review.status = status
            review.feedback = feedback
            review.locked = status == "Approved"
            break
    st.session_state["feature_reviews"] = reviews


def rejected_reviews_missing_feedback() -> list[FeatureReview]:
    return [
        review
        for review in st.session_state.get("feature_reviews", [])
        if review.status == "Rejected" and not review.feedback.strip()
    ]


def rejected_reviews_ready_for_regeneration() -> list[FeatureReview]:
    return [
        review
        for review in st.session_state.get("feature_reviews", [])
        if review.status == "Rejected" and review.feedback.strip()
    ]

with st.sidebar:
    st.header("Configuration")
    api_key_available = bool(os.getenv("OPENAI_API_KEY"))
    model_available = bool(os.getenv("OPENAI_MODEL"))
    temperature_available = bool(os.getenv("OPENAI_TEMPERATURE"))
    st.write("OpenAI API key:", "Configured" if api_key_available else "Missing")
    st.write("OpenAI model:", os.getenv("OPENAI_MODEL") if model_available else "Missing")
    st.write("Temperature:", os.getenv("OPENAI_TEMPERATURE") if temperature_available else "Missing")

with st.form("epic_form"):
    title = st.text_input("Epic Title", placeholder="AI-Powered Resource Matching")
    description = st.text_area(
        "Epic Description",
        placeholder="Provide intelligent recommendations for matching resources to projects.",
        height=120,
    )
    business_context = st.text_area(
        "Business Context",
        placeholder="Resource managers spend significant time manually identifying suitable resources.",
        height=120,
    )
    success_metrics = st.text_area(
        "Success Metrics",
        placeholder="Reduce staffing effort by 30%.\nIncrease project fulfillment accuracy by 20%.",
        height=100,
    )

    submitted = st.form_submit_button("Generate Features", type="primary")

if submitted:
    if not all([title, description, business_context, success_metrics]):
        st.error("Please complete all Epic fields before generating Features.")
    elif not all([api_key_available, model_available, temperature_available]):
        st.error("Set OPENAI_API_KEY, OPENAI_MODEL, and OPENAI_TEMPERATURE before generating Features.")
    else:
        epic = Epic(
            title=title,
            description=description,
            business_context=business_context,
            success_metrics=success_metrics,
        )

        with st.spinner("Generating Features..."):
            try:
                result = run_workflow(epic)
            except Exception as exc:
                st.error(f"Feature generation failed: {exc}")
            else:
                st.session_state["epic"] = epic
                st.session_state["feature_set"] = result["feature_set"]
                st.session_state["evaluation_result"] = result["evaluation_result"]
                st.session_state["feature_reviews"] = initialize_feature_reviews(
                    len(result["feature_set"].features)
                )

feature_set = st.session_state.get("feature_set")
evaluation_result = st.session_state.get("evaluation_result")
feature_reviews = st.session_state.get("feature_reviews", [])
review_by_index = reviews_by_index()
evaluations_by_feature = {}
if evaluation_result:
    evaluations_by_feature = {
        evaluation.feature_name: evaluation for evaluation in evaluation_result.evaluations
    }

if feature_set:
    st.subheader("Generated Features")

    for index, feature in enumerate(feature_set.features, start=1):
        feature_index = index - 1
        review = review_by_index.get(feature_index, FeatureReview(feature_index=feature_index))
        with st.expander(f"{index}. {feature.name} - v{feature.version}", expanded=True):
            status_label = f"{review.status}"
            if review.locked:
                status_label = f"{status_label} / Locked"
            st.markdown(f"**Review Status:** {status_label}")
            st.markdown(f"**Description**\n\n{feature.description}")
            st.markdown(f"**Business Value**\n\n{feature.business_value}")
            st.markdown("**Acceptance Criteria**")
            for criterion in feature.acceptance_criteria:
                st.markdown(f"- {criterion}")

            if feature.revision_summary:
                st.markdown("**Revision Summary**")
                for summary_item in feature.revision_summary:
                    st.markdown(f"- {summary_item}")

            evaluation = evaluations_by_feature.get(feature.name)
            if evaluation:
                st.markdown("**Evaluation Recommendation**")
                if evaluation.recommendation == "APPROVE":
                    st.success(evaluation.recommendation)
                else:
                    st.warning(evaluation.recommendation)

                st.markdown("**Findings**")
                for finding in evaluation.findings:
                    st.markdown(f"- {finding}")

            if review.status == "Approved":
                st.info("Approved Feature is locked and will not be regenerated.")
            else:
                st.markdown("**Human Review**")
                approve_col, reject_col = st.columns(2)
                with approve_col:
                    if st.button("Approve", key=f"approve_{feature_index}"):
                        set_review_status(feature_index, "Approved")
                        st.rerun()
                feedback_key = f"reject_feedback_{feature_index}"
                feedback_value = st.text_area(
                    "Rejection Feedback",
                    value=review.feedback,
                    key=feedback_key,
                    placeholder="Explain what should change before this Feature is regenerated.",
                )
                with reject_col:
                    reject_disabled = not feedback_value.strip()
                    if st.button(
                        "Reject",
                        key=f"reject_{feature_index}",
                        disabled=reject_disabled,
                    ):
                        set_review_status(feature_index, "Rejected", feedback_value.strip())
                        st.rerun()

                if review.status == "Rejected":
                    if review.feedback.strip():
                        st.warning("Rejected / Ready for Regeneration")
                    else:
                        st.warning("Rejected / Feedback Required")

    rejected_ready = rejected_reviews_ready_for_regeneration()
    rejected_missing_feedback = rejected_reviews_missing_feedback()
    if feature_reviews:
        st.divider()
        if rejected_missing_feedback:
            st.warning("All rejected Features require feedback before regeneration.")

        regenerate_disabled = not rejected_ready or bool(rejected_missing_feedback)
        if st.button(
            "Regenerate Rejected Features",
            type="primary",
            disabled=regenerate_disabled,
        ):
            with st.spinner("Regenerating rejected Features..."):
                try:
                    result = run_regeneration_workflow(
                        epic=st.session_state["epic"],
                        feature_set=st.session_state["feature_set"],
                        evaluation_result=st.session_state["evaluation_result"],
                        feature_reviews=st.session_state["feature_reviews"],
                    )
                except Exception as exc:
                    st.error(f"Feature regeneration failed: {exc}")
                else:
                    st.session_state["feature_set"] = result["feature_set"]
                    st.session_state["evaluation_result"] = result["evaluation_result"]
                    st.session_state["feature_reviews"] = result["feature_reviews"]
                    st.rerun()
else:
    st.info("Enter an Epic and generate Features to begin.")
