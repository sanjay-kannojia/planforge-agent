import hashlib
import json
import math
import re
from datetime import datetime, timezone
from uuid import uuid4

from src.config.settings import get_settings
from src.models.epic import Epic
from src.models.evaluation_result import EvaluationResult
from src.models.feature import Feature
from src.models.feature_set import FeatureSet
from src.models.learning_artifact import (
    EpicDecompositionArtifact,
    FeatureEvaluationSummary,
    FeatureReviewHistoryEntry,
    FeatureVersionHistorySummary,
    RejectedFeatureLesson,
)
from src.models.retrieval_context import (
    RetrievalContext,
    RetrievedEpicArtifact,
    RetrievedRejectedLesson,
)


class LearningRepositoryService:
    EMBEDDING_DIMENSIONS = 256

    def __init__(self) -> None:
        try:
            import chromadb
        except ImportError as exc:
            raise ValueError(
                "chromadb is required for Milestone 4 learning retrieval. "
                "Install dependencies from requirements.txt."
            ) from exc

        settings = get_settings()
        self.client = chromadb.PersistentClient(path=settings.chroma_db_path)
        self.epic_collection = self.client.get_or_create_collection(
            settings.chroma_epic_decompositions_collection
        )
        self.lesson_collection = self.client.get_or_create_collection(
            settings.chroma_rejected_feature_lessons_collection
        )

    def retrieve_similar_artifacts(self, epic: Epic, limit: int = 3) -> RetrievalContext:
        results = self.epic_collection.query(
            query_embeddings=[self._embed_text(self._epic_query_text(epic))],
            n_results=limit,
            where={"status": "approved"},
        )
        return RetrievalContext(similar_artifacts=self._parse_artifact_results(results))

    def retrieve_rejected_lessons(
        self,
        epic: Epic,
        rejected_feature: Feature,
        human_rejection_feedback: str,
        limit: int = 5,
    ) -> RetrievalContext:
        query_text = "\n".join(
            [
                self._epic_query_text(epic),
                f"Rejected Feature: {rejected_feature.name}",
                rejected_feature.description,
                f"Human Feedback: {human_rejection_feedback}",
            ]
        )
        results = self.lesson_collection.query(
            query_embeddings=[self._embed_text(query_text)],
            n_results=limit,
            where={"artifact_type": "rejected_feature_lesson"},
        )
        return RetrievalContext(rejected_lessons=self._parse_lesson_results(results))

    def store_completed_artifact(
        self,
        epic: Epic,
        feature_set: FeatureSet,
        evaluation_result: EvaluationResult,
        review_history: list[FeatureReviewHistoryEntry],
    ) -> EpicDecompositionArtifact:
        artifact = self._build_artifact(
            epic=epic,
            feature_set=feature_set,
            evaluation_result=evaluation_result,
            review_history=review_history,
        )
        self._validate_approved_artifact_for_storage(artifact)
        artifact_id = f"epic-decomposition-{uuid4()}"
        artifact_document = artifact.model_dump_json()
        self.epic_collection.add(
            ids=[artifact_id],
            documents=[self._artifact_document_text(artifact)],
            embeddings=[self._embed_text(self._artifact_document_text(artifact))],
            metadatas=[artifact.metadata | {"artifact_json": artifact_document}],
        )

        lessons = [
            lesson
            for lesson in artifact.rejected_feature_lessons
            if lesson.human_feedback.strip()
        ]
        if lessons:
            self.lesson_collection.add(
                ids=[f"rejected-feature-lesson-{uuid4()}" for _ in lessons],
                documents=[
                    self._lesson_document_text(epic=artifact.epic, lesson=lesson)
                    for lesson in lessons
                ],
                embeddings=[
                    self._embed_text(self._lesson_document_text(epic=artifact.epic, lesson=lesson))
                    for lesson in lessons
                ],
                metadatas=[
                    {
                        "artifact_type": "rejected_feature_lesson",
                        "epic_title": artifact.epic.title,
                        "feature_name": lesson.original_feature_name,
                        "status": "approved",
                        "source": "PlanForge",
                        "lesson_json": lesson.model_dump_json(),
                    }
                    for lesson in lessons
                ],
            )

        return artifact

    def _validate_approved_artifact_for_storage(
        self,
        artifact: EpicDecompositionArtifact,
    ) -> None:
        if artifact.metadata.get("status") != "approved":
            raise ValueError(
                "Learning artifacts can only be stored after the Epic Decomposition "
                "Artifact has approved status."
            )

        if not artifact.final_approved_features:
            raise ValueError(
                "Learning artifacts can only be stored when at least one final approved "
                "Feature is present."
            )

        non_approved_summaries = [
            summary
            for summary in artifact.version_history_summary
            if summary.final_status != "Approved"
        ]
        if non_approved_summaries:
            raise ValueError(
                "Learning artifacts can only be stored when every Feature version "
                "history summary has final status Approved."
            )

    def _build_artifact(
        self,
        epic: Epic,
        feature_set: FeatureSet,
        evaluation_result: EvaluationResult,
        review_history: list[FeatureReviewHistoryEntry],
    ) -> EpicDecompositionArtifact:
        created_at = datetime.now(timezone.utc).isoformat()
        return EpicDecompositionArtifact(
            epic=epic,
            final_approved_features=feature_set.features,
            rejected_feature_lessons=self._build_rejected_lessons(
                feature_set=feature_set,
                review_history=review_history,
            ),
            human_rejection_feedback=[
                entry.feedback
                for entry in review_history
                if entry.status == "Rejected" and entry.feedback.strip()
            ],
            ai_evaluations=[
                FeatureEvaluationSummary(
                    feature_name=evaluation.feature_name,
                    recommendation=evaluation.recommendation,
                    findings=evaluation.findings,
                )
                for evaluation in evaluation_result.evaluations
            ],
            version_history_summary=self._build_version_history(
                feature_set=feature_set,
                review_history=review_history,
            ),
            metadata={
                "artifact_type": "epic_decomposition",
                "status": "approved",
                "domain": "",
                "created_at": created_at,
                "feature_count": len(feature_set.features),
                "source": "PlanForge",
            },
        )

    def _build_rejected_lessons(
        self,
        feature_set: FeatureSet,
        review_history: list[FeatureReviewHistoryEntry],
    ) -> list[RejectedFeatureLesson]:
        lessons = []
        for entry in review_history:
            if entry.status != "Rejected" or not entry.feedback.strip():
                continue

            replacement = feature_set.features[entry.feature_index]
            lessons.append(
                RejectedFeatureLesson(
                    original_feature_name=entry.feature_name,
                    rejected_version=entry.feature_version,
                    description=entry.feature_snapshot.description,
                    business_value=entry.feature_snapshot.business_value,
                    human_feedback=entry.feedback,
                    ai_findings=entry.ai_findings,
                    replacement_feature_name=replacement.name,
                    final_resolution=(
                        f"Replaced by approved Feature '{replacement.name}' "
                        f"at version {replacement.version}."
                    ),
                )
            )
        return lessons

    def _build_version_history(
        self,
        feature_set: FeatureSet,
        review_history: list[FeatureReviewHistoryEntry],
    ) -> list[FeatureVersionHistorySummary]:
        summaries = []
        for index, final_feature in enumerate(feature_set.features):
            versions = {
                entry.feature_version
                for entry in review_history
                if entry.feature_index == index
            }
            versions.add(final_feature.version)
            summaries.append(
                FeatureVersionHistorySummary(
                    feature_name=final_feature.name,
                    versions=sorted(versions),
                    final_status="Approved",
                )
            )
        return summaries

    def _parse_artifact_results(self, results) -> list[RetrievedEpicArtifact]:
        artifacts = []
        for metadata in self._first_result_metadatas(results):
            artifact_json = metadata.get("artifact_json")
            if not artifact_json:
                continue
            artifact = EpicDecompositionArtifact.model_validate_json(artifact_json)
            artifacts.append(
                RetrievedEpicArtifact(
                    epic_title=artifact.epic.title,
                    epic_summary=artifact.epic.description,
                    final_feature_names=[
                        feature.name for feature in artifact.final_approved_features
                    ],
                    rejected_lessons=[
                        self._to_retrieved_lesson(artifact.epic.title, lesson)
                        for lesson in artifact.rejected_feature_lessons
                        if lesson.human_feedback.strip()
                    ],
                )
            )
        return artifacts

    def _parse_lesson_results(self, results) -> list[RetrievedRejectedLesson]:
        lessons = []
        for metadata in self._first_result_metadatas(results):
            lesson_json = metadata.get("lesson_json")
            epic_title = metadata.get("epic_title", "")
            if not lesson_json:
                continue
            lesson = RejectedFeatureLesson.model_validate_json(lesson_json)
            lessons.append(self._to_retrieved_lesson(epic_title, lesson))
        return lessons

    def _to_retrieved_lesson(
        self,
        epic_title: str,
        lesson: RejectedFeatureLesson,
    ) -> RetrievedRejectedLesson:
        return RetrievedRejectedLesson(
            epic_title=epic_title or "Unknown Epic",
            original_feature_name=lesson.original_feature_name,
            human_feedback=lesson.human_feedback,
            final_resolution=lesson.final_resolution,
            replacement_feature_name=lesson.replacement_feature_name,
        )

    def _first_result_metadatas(self, results) -> list[dict]:
        metadatas = results.get("metadatas") or []
        if not metadatas:
            return []
        return [metadata for metadata in metadatas[0] if metadata]

    def _epic_query_text(self, epic: Epic) -> str:
        return "\n".join(
            [
                f"Epic Title: {epic.title}",
                f"Epic Description: {epic.description}",
                f"Business Context: {epic.business_context}",
                f"Success Metrics: {epic.success_metrics}",
            ]
        )

    def _artifact_document_text(self, artifact: EpicDecompositionArtifact) -> str:
        feature_names = "\n".join(
            f"- {feature.name}: {feature.description}"
            for feature in artifact.final_approved_features
        )
        lessons = "\n".join(
            f"- {lesson.original_feature_name}: {lesson.human_feedback}"
            for lesson in artifact.rejected_feature_lessons
        )
        return "\n".join(
            [
                self._epic_query_text(artifact.epic),
                "Final Approved Features:",
                feature_names,
                "Rejected Feature Lessons:",
                lessons or "- None",
            ]
        )

    def _lesson_document_text(self, epic: Epic, lesson: RejectedFeatureLesson) -> str:
        return "\n".join(
            [
                f"Epic Title: {epic.title}",
                f"Rejected Feature: {lesson.original_feature_name}",
                f"Description: {lesson.description}",
                f"Business Value: {lesson.business_value}",
                f"Human Feedback: {lesson.human_feedback}",
                f"AI Findings: {json.dumps(lesson.ai_findings)}",
                f"Final Resolution: {lesson.final_resolution}",
            ]
        )

    def _embed_text(self, text: str) -> list[float]:
        tokens = re.findall(r"[a-z0-9]+", text.lower())
        vector = [0.0] * self.EMBEDDING_DIMENSIONS

        for token in tokens:
            self._add_token_to_vector(vector, token, 1.0)
        for first, second in zip(tokens, tokens[1:]):
            self._add_token_to_vector(vector, f"{first}_{second}", 1.5)

        magnitude = math.sqrt(sum(value * value for value in vector))
        if magnitude == 0:
            return vector
        return [value / magnitude for value in vector]

    def _add_token_to_vector(self, vector: list[float], token: str, weight: float) -> None:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % self.EMBEDDING_DIMENSIONS
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[index] += sign * weight
