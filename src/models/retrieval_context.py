from pydantic import BaseModel, Field


class RetrievedRejectedLesson(BaseModel):
    epic_title: str = Field(..., min_length=1)
    original_feature_name: str = Field(..., min_length=1)
    human_feedback: str = Field(..., min_length=1)
    final_resolution: str = Field(..., min_length=1)
    replacement_feature_name: str = ""


class RetrievedEpicArtifact(BaseModel):
    epic_title: str = Field(..., min_length=1)
    epic_summary: str = Field(..., min_length=1)
    final_feature_names: list[str] = Field(default_factory=list)
    rejected_lessons: list[RetrievedRejectedLesson] = Field(default_factory=list)


class RetrievalContext(BaseModel):
    similar_artifacts: list[RetrievedEpicArtifact] = Field(default_factory=list)
    rejected_lessons: list[RetrievedRejectedLesson] = Field(default_factory=list)

    def has_context(self) -> bool:
        return bool(self.similar_artifacts or self.rejected_lessons)
