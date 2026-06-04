from pydantic import BaseModel, Field


class Epic(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    business_context: str = Field(..., min_length=1)
    success_metrics: str = Field(..., min_length=1)
