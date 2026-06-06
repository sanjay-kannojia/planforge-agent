import os

import streamlit as st
from dotenv import load_dotenv

from src.graph.workflow import run_workflow
from src.models.epic import Epic


load_dotenv()


st.set_page_config(page_title="PlanForge", layout="wide")

st.title("PlanForge")
st.caption("Epic to Feature generation")

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
                st.session_state["feature_set"] = result["feature_set"]
                st.session_state["evaluation_result"] = result["evaluation_result"]

feature_set = st.session_state.get("feature_set")
evaluation_result = st.session_state.get("evaluation_result")
evaluations_by_feature = {}
if evaluation_result:
    evaluations_by_feature = {
        evaluation.feature_name: evaluation for evaluation in evaluation_result.evaluations
    }

if feature_set:
    st.subheader("Generated Features")

    for index, feature in enumerate(feature_set.features, start=1):
        with st.expander(f"{index}. {feature.name}", expanded=True):
            st.markdown(f"**Description**\n\n{feature.description}")
            st.markdown(f"**Business Value**\n\n{feature.business_value}")
            st.markdown("**Acceptance Criteria**")
            for criterion in feature.acceptance_criteria:
                st.markdown(f"- {criterion}")

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
else:
    st.info("Enter an Epic and generate Features to begin.")
