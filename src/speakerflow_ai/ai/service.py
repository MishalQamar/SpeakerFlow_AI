import json
from typing import Protocol

from openai import AsyncOpenAI
from web_app.config import load_config

from .models import (
    AIReviewRecommendation,
    SpeakingRequestAnalysisInput,
    SpeakingRequestAnalysisResult,
)


class SpeakingRequestAnalyzer(Protocol):
    async def analyze(
        self, analysis_input: SpeakingRequestAnalysisInput
    ) -> SpeakingRequestAnalysisResult:
        """
        Analyze a speaking request and return a structured review result.
        """
        ...


class MockSpeakingRequestAnalyzer:
    async def analyze(
        self, analysis_input: SpeakingRequestAnalysisInput
    ) -> SpeakingRequestAnalysisResult:
        speaking_request = analysis_input.speaking_request

        missing_information: list[str] = []

        if not speaking_request.topic.strip():
            missing_information.append("Topic is missing.")

        if speaking_request.duration_in_minutes > 90:
            recommendation = AIReviewRecommendation.REJECT
            rationale = "The requested talk duration is longer than the supported limit."
        elif speaking_request.duration_in_minutes < 20:
            recommendation = AIReviewRecommendation.REJECT
            rationale = "The requested talk duration is shorter than the supported minimum."
        elif missing_information:
            recommendation = AIReviewRecommendation.REVIEW
            rationale = "Important request details are missing and should be reviewed."
        else:
            recommendation = AIReviewRecommendation.REVIEW
            rationale = "The request looks plausible, but a human should still review it."

        summary = (
            f"Request for topic '{speaking_request.topic}' "
            f"with duration {speaking_request.duration_in_minutes} minutes "
            f"from {speaking_request.requester_email}."
        )

        return SpeakingRequestAnalysisResult(
            summary=summary,
            missing_information=missing_information,
            recommendation=recommendation,
            rationale=rationale,
        )


class OpenAISpeakingRequestAnalyzer:
    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
    ):
        config = load_config()
        self.api_key = api_key or config.OPENAI_API_KEY
        self.model = model or config.OPENAI_MODEL

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not set.")

        self.client = AsyncOpenAI(api_key=self.api_key)

    async def analyze(
        self, analysis_input: SpeakingRequestAnalysisInput
    ) -> SpeakingRequestAnalysisResult:
        speaking_request = analysis_input.speaking_request

        schema = SpeakingRequestAnalysisResult.model_json_schema()

        prompt = f"""
You are an expert speaking-request reviewer for a production speaking management platform.

Review this request carefully and return a structured result.

Business guidance:
- If duration is greater than 90 minutes, recommend REJECT.
- If duration is less than 20 minutes, recommend REJECT.
- If important context seems missing, prefer REVIEW.
- Do not invent facts.
- Keep the summary and rationale concise and professional.

Speaking request:
- id: {speaking_request.id}
- event_time: {speaking_request.event_time.isoformat()}
- topic: {speaking_request.topic}
- duration_in_minutes: {speaking_request.duration_in_minutes}
- requester_email: {speaking_request.requester_email}
- address.street: {speaking_request.address.street}
- address.city: {speaking_request.address.city}
- address.state: {speaking_request.address.state}
- address.country: {speaking_request.address.country}

Return valid JSON matching the provided schema.
""".strip()

        response = await self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "You produce only structured JSON that matches the requested schema.",
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": prompt,
                        }
                    ],
                },
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "speaking_request_analysis",
                    "schema": schema,
                    "strict": True,
                }
            },
        )

        parsed = json.loads(response.output_text)
        return SpeakingRequestAnalysisResult.model_validate(parsed)
