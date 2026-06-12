from pydantic import BaseModel, Field

from src.models.epic import Epic
from src.models.feature import Feature


class FeatureReviewHistoryEntry(BaseModel):
    feature_index: int = Field(..., ge=0)
    feature_name: str = Field(..., min_length=1)
    feature_version: int = Field(..., ge=1)
    status: str = Field(..., min_length=1)
    feedback: str = ""
    ai_findings: list[str] = Field(default_factory=list)
    revision_summary: list[str] = Field(default_factory=list)
    feature_snapshot: Feature


class RejectedFeatureLesson(BaseModel):
    original_feature_name: str = Field(..., min_length=1)
    rejected_version: int = Field(..., ge=1)
    description: str = Field(..., min_length=1)
    business_value: str = Field(..., min_length=1)
    human_feedback: str = Field(..., min_length=1)
    ai_findings: list[str] = Field(default_factory=list)
    replacement_feature_name: str = ""
    final_resolution: str = Field(..., min_length=1)


class FeatureEvaluationSummary(BaseModel):
    feature_name: str = Field(..., min_length=1)
    recommendation: str = Field(..., min_length=1)
    findings: list[str] = Field(default_factory=list)


class FeatureVersionHistorySummary(BaseModel):
    feature_name: str = Field(..., min_length=1)
    versions: list[int] = Field(default_factory=list)
    final_status: str = Field(..., min_length=1)


class EpicDecompositionArtifact(BaseModel):
    artifact_type: str = "epic_decomposition"
    epic: Epic
    final_approved_features: list[Feature] = Field(..., min_length=1)
    rejected_feature_lessons: list[RejectedFeatureLesson] = Field(default_factory=list)
    human_rejection_feedback: list[str] = Field(default_factory=list)
    ai_evaluations: list[FeatureEvaluationSummary] = Field(default_factory=list)
    version_history_summary: list[FeatureVersionHistorySummary] = Field(default_factory=list)
    metadata: dict[str, str | int] = Field(default_factory=dict)
