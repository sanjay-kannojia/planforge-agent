import json

from openai import OpenAI
from pydantic import ValidationError

from src.config.settings import get_settings
from src.models.epic import Epic
from src.models.feature_set import FeatureSet
from src.models.retrieval_context import RetrievalContext
from src.prompts.feature_generator import build_feature_generation_prompt


class OpenAIService:
    def __init__(self) -> None:
        settings = get_settings()
        self.api_key = settings.openai_api_key
        self.model = settings.openai_model
        self.temperature = settings.openai_temperature
        self.client = OpenAI(api_key=self.api_key)

    def generate_features(
        self,
        epic: Epic,
        learning_context: RetrievalContext | None = None,
    ) -> FeatureSet:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": build_feature_generation_prompt(epic, learning_context),
                },
            ],
            response_format={"type": "json_object"},
            temperature=self.temperature,
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("OpenAI returned an empty response.")

        return self.validate_feature_set_response(content)

    def validate_feature_set_response(self, content: str) -> FeatureSet:
        try:
            payload = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError("OpenAI response was not valid JSON.") from exc

        try:
            return FeatureSet.model_validate(payload)
        except ValidationError as exc:
            raise ValueError("OpenAI response did not match the FeatureSet schema.") from exc
