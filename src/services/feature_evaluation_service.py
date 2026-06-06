import json

from pydantic import ValidationError

from src.models.epic import Epic
from src.models.evaluation_result import EvaluationResult
from src.models.feature_set import FeatureSet
from src.prompts.feature_evaluation import build_feature_set_evaluation_prompt
from src.services.llm_service import OpenAIService


class FeatureEvaluationService(OpenAIService):
    def evaluate_features(self, epic: Epic, feature_set: FeatureSet) -> EvaluationResult:
        prompt = build_feature_set_evaluation_prompt(epic=epic, feature_set=feature_set)
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
            raise ValueError("OpenAI returned an empty feature-set evaluation response.")

        evaluation_result = self.validate_evaluation_result_response(content)
        self._validate_evaluation_coverage(feature_set, evaluation_result)
        return evaluation_result

    def validate_evaluation_result_response(self, content: str) -> EvaluationResult:
        try:
            payload = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError("OpenAI feature evaluation response was not valid JSON.") from exc

        try:
            return EvaluationResult.model_validate(payload)
        except ValidationError as exc:
            raise ValueError(
                "OpenAI feature evaluation response did not match the EvaluationResult schema."
            ) from exc

    def _validate_evaluation_coverage(
        self,
        feature_set: FeatureSet,
        evaluation_result: EvaluationResult,
    ) -> None:
        expected_names = {feature.name for feature in feature_set.features}
        actual_names = {evaluation.feature_name for evaluation in evaluation_result.evaluations}

        if actual_names != expected_names:
            raise ValueError(
                "OpenAI feature evaluation response must include exactly one evaluation per Feature."
            )

        if len(evaluation_result.evaluations) != len(feature_set.features):
            raise ValueError(
                "OpenAI feature evaluation response must not include duplicate Feature evaluations."
            )
