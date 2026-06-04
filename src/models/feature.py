from pydantic import BaseModel, Field


class Feature(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    business_value: str = Field(..., min_length=1)
    acceptance_criteria: list[str] = Field(..., min_length=1)
