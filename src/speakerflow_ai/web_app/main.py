import uuid

from fastapi import FastAPI

from speakerflow_ai.web_app.api_requests import (
    AcceptSpeakingRequest,
    RejectSpeakingRequest,
    SubmitSpeakingRequest,
)
from speakerflow_ai.web_app.config import load_config
from speakerflow_ai.web_app.responses import SpeakingRequestDetails

app = FastAPI()
app_config = load_config()


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


@app.post(
    "/speaking-requests/accept/",
    status_code=200,
    response_model=SpeakingRequestDetails,
)
def accept_speaking_request(accept_speaking_request_body: AcceptSpeakingRequest):
    return {
        "id": accept_speaking_request_body.id,
        "event_time": "2026-05-10T14:30:00",
        "address": {
            "street": "Sunny Street 42",
            "city": "Dublin",
            "state": "Leinster",
            "country": "Ireland",
        },
        "topic": "Production-ready FastAPI",
        "duration_in_minutes": 45,
        "requester_email": "john@doe.com",
        "status": "ACCEPTED",
    }


@app.post(
    "/speaking-requests/reject/",
    status_code=200,
    response_model=SpeakingRequestDetails,
)
def reject_speaking_request(reject_speaking_request_body: RejectSpeakingRequest):
    return {
        "id": reject_speaking_request_body.id,
        "event_time": "2026-05-10T14:30:00",
        "address": {
            "street": "Sunny Street 42",
            "city": "Dublin",
            "state": "Leinster",
            "country": "Ireland",
        },
        "topic": "Production-ready FastAPI",
        "duration_in_minutes": 45,
        "requester_email": "john@doe.com",
        "status": "REJECTED",
    }
