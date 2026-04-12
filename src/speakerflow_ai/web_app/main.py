import uuid

from fastapi import FastAPI

from speakerflow_ai.web_app.api_requests import SubmitSpeakingRequest
from speakerflow_ai.web_app.responses import SpeakingRequestDetails

app = FastAPI()


@app.get("/health-check/")
def health_check():
    return {"message": "OK"}


@app.post("/request-speaking/", status_code=201, response_model=SpeakingRequestDetails)
def request_speaking(submit_speaking_request: SubmitSpeakingRequest):
    return {
        "id": str(uuid.uuid4()),
        "event_time": submit_speaking_request.event_time,
        "address": submit_speaking_request.address,
        "topic": submit_speaking_request.topic,
        "duration_in_minutes": submit_speaking_request.duration_in_minutes,
        "requester_email": submit_speaking_request.requester_email,
        "status": "PENDING",
    }
