import json

from pydantic import ValidationError

from src.models.epic import Epic
from src.models.feature import Feature
from src.models.regeneration_result import RegenerationResult
from src.prompts.feature_regeneration import build_feature_regeneration_prompt
from src.services.llm_service import OpenAIService


class FeatureRegenerationService(OpenAIService):
    def regenerate_feature(
        self,
        epic: Epic,
        rejected_feature: Feature,
        ai_evaluation_findings: list[str],
        human_rejection_feedback: str,
        approved_features: list[Feature],
    ) -> RegenerationResult:
        if not human_rejection_feedback.strip():
            raise ValueError("Human rejection feedback is required before regeneration.")

        prompt = build_feature_regeneration_prompt(
            epic=epic,
            rejected_feature=rejected_feature,
            ai_evaluation_findings=ai_evaluation_findings,
            human_rejection_feedback=human_rejection_feedback,
            approved_features=approved_features,
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=self.temperature,
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("OpenAI returned an empty feature regeneration response.")

        return self.validate_regeneration_result_response(content)

    def validate_regeneration_result_response(self, content: str) -> RegenerationResult:
        try:
            payload = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError("OpenAI feature regeneration response was not valid JSON.") from exc

        try:
            return RegenerationResult.model_validate(payload)
        except ValidationError as exc:
            raise ValueError(
                "OpenAI feature regeneration response did not match the RegenerationResult schema."
            ) from exc
