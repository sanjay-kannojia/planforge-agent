import json
import os

from openai import OpenAI
from pydantic import ValidationError

from src.models.epic import Epic
from src.models.feature_set import FeatureSet
from src.prompts.feature_generator import build_feature_generation_prompt


class OpenAIService:
    def __init__(self) -> None:
        self.api_key = self._required_env("OPENAI_API_KEY")
        self.model = self._required_env("OPENAI_MODEL")
        self.temperature = self._required_float_env("OPENAI_TEMPERATURE")
        self.client = OpenAI(api_key=self.api_key)

    def generate_features(self, epic: Epic) -> FeatureSet:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": build_feature_generation_prompt(epic)},
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

    def _required_env(self, name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise ValueError(f"{name} must be configured in the environment or .env file.")
        return value

    def _required_float_env(self, name: str) -> float:
        value = self._required_env(name)
        try:
            return float(value)
        except ValueError as exc:
            raise ValueError(f"{name} must be a valid number.") from exc
