from enum import Enum

from pydantic import BaseModel, Field

from speakerflow_ai.models import SpeakingRequest


class AIReviewRecommendation(str, Enum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    REVIEW = "REVIEW"


class SpeakingRequestAnalysisInput(BaseModel):
    speaking_request: SpeakingRequest


class SpeakingRequestAnalysisResult(BaseModel):
    summary: str = Field(
        ...,
        description="A short summary of the speaking request.",
    )
    missing_information: list[str] = Field(
        default_factory=list,
        description="Important information the AI thinks is missing.",
    )
    recommendation: AIReviewRecommendation
    rationale: str = Field(
        ...,
        description="A short explanation for the recommendation.",
    )
