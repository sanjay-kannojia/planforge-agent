import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

import streamlit as st
from dotenv import load_dotenv


load_dotenv()

# Safe, non-secret defaults for local and prototype deployments.
DEFAULT_CHROMA_DB_PATH = "./chroma_db"
DEFAULT_EPIC_DECOMPOSITIONS_COLLECTION = "epic_decompositions"
DEFAULT_REJECTED_FEATURE_LESSONS_COLLECTION = "rejected_feature_lessons"


@dataclass(frozen=True)
class AppSettings:
    openai_api_key: str
    openai_model: str
    openai_temperature: float
    llm_provider: str
    chroma_db_path: str
    chroma_epic_decompositions_collection: str
    chroma_rejected_feature_lessons_collection: str


def get_config_value(name: str, default: Any = None) -> Any:
    """Read configuration from .env/environment first, then Streamlit secrets."""
    env_value = os.getenv(name)

    if env_value is not None and str(env_value).strip():
        return env_value

    try:
        return st.secrets.get(name, default)
    except (FileNotFoundError, KeyError):
        return default


def get_required_config(name: str) -> str:
    """Return a required setting or raise a clear configuration error."""
    value = get_config_value(name)

    if value is None or not str(value).strip():
        raise ValueError(
            f"{name} must be configured in the local .env file "
            "or Streamlit Community Cloud secrets."
        )

    return str(value)


def get_required_float_config(name: str) -> float:
    """Return a required numeric setting or raise a clear configuration error."""
    value = get_required_config(name)
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(
            f"{name} must be a valid number in the local .env file "
            "or Streamlit Community Cloud secrets."
        ) from exc


@lru_cache
def get_settings() -> AppSettings:
    """Build typed application settings from local config or Streamlit secrets."""
    return AppSettings(
        openai_api_key=get_required_config("OPENAI_API_KEY"),
        openai_model=get_required_config("OPENAI_MODEL"),
        openai_temperature=get_required_float_config("OPENAI_TEMPERATURE"),
        llm_provider=str(get_config_value("LLM_PROVIDER", "openai")),
        chroma_db_path=str(get_config_value("CHROMA_DB_PATH", DEFAULT_CHROMA_DB_PATH)),
        chroma_epic_decompositions_collection=str(
            get_config_value(
                "CHROMA_COLLECTION_EPIC_DECOMPOSITIONS",
                DEFAULT_EPIC_DECOMPOSITIONS_COLLECTION,
            )
        ),
        chroma_rejected_feature_lessons_collection=str(
            get_config_value(
                "CHROMA_COLLECTION_REJECTED_FEATURE_LESSONS",
                DEFAULT_REJECTED_FEATURE_LESSONS_COLLECTION,
            )
        ),
    )
