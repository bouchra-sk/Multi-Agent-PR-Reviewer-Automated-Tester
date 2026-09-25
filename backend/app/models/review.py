from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    code: str = Field(min_length=1)
    language: str = "python"


class ReviewResponse(BaseModel):
    summary: dict[str, object]
    findings: list[dict[str, object]]
    agent: str
    language: str