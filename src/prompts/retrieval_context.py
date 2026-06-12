from src.models.learning_artifact import FeatureReviewHistoryEntry
from src.models.retrieval_context import RetrievalContext


def format_retrieval_context_for_generation(context: RetrievalContext | None) -> str:
    if context is None or not context.has_context():
        return "No prior approved decomposition artifacts were retrieved."

    sections = []
    for index, artifact in enumerate(context.similar_artifacts, start=1):
        feature_names = "\n".join(f"- {name}" for name in artifact.final_feature_names) or "- None"
        rejected_lessons = _format_rejected_lessons(artifact.rejected_lessons)
        sections.append(
            f"""Similar Approved Epic {index}
Title: {artifact.epic_title}
Summary: {artifact.epic_summary}
Final Approved Feature Pattern:
{feature_names}
Rejected Lessons From That Session:
{rejected_lessons}"""
        )

    if context.rejected_lessons:
        sections.append(
            "Additional Relevant Rejected Lessons:\n"
            f"{_format_rejected_lessons(context.rejected_lessons)}"
        )

    return "\n\n".join(sections)


def format_retrieval_context_for_regeneration(context: RetrievalContext | None) -> str:
    if context is None or not context.has_context():
        return "No prior rejected Feature lessons were retrieved."

    sections = []
    if context.similar_artifacts:
        sections.append(format_retrieval_context_for_generation(context))
    if context.rejected_lessons:
        sections.append(
            "Relevant Rejected Feature Lessons:\n"
            f"{_format_rejected_lessons(context.rejected_lessons)}"
        )
    return "\n\n".join(sections)


def format_review_history_for_regeneration(
    history_entries: list[FeatureReviewHistoryEntry],
) -> str:
    if not history_entries:
        return "No prior rejection attempts for this Feature in the current session."

    sections = []
    for entry in history_entries:
        findings = "\n".join(f"- {finding}" for finding in entry.ai_findings) or "- None"
        sections.append(
            f"""Feature v{entry.feature_version}
Name: {entry.feature_name}
Status: {entry.status}
Human Feedback: {entry.feedback}
AI Findings:
{findings}"""
        )
    return "\n\n".join(sections)


def _format_rejected_lessons(lessons) -> str:
    if not lessons:
        return "- None"

    return "\n".join(
        [
            f"- {lesson.original_feature_name}: feedback='{lesson.human_feedback}', "
            f"resolution='{lesson.final_resolution}', replacement='{lesson.replacement_feature_name or 'None'}'"
            for lesson in lessons
        ]
    )
