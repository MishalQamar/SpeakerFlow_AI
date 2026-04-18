import uuid
from pathlib import Path

from ai import run_speaking_request_review_with_openai
from ai.models import SpeakingRequestAnalysisInput, SpeakingRequestAnalysisResult
from alembic import config, script
from alembic.runtime import migration
from database import speaking_request_db
from fastapi import Depends, FastAPI, Response
from models import SpeakingRequest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .api_requests import (
    AcceptSpeakingRequest,
    RejectSpeakingRequest,
    SubmitSpeakingRequest,
)
from .config import load_config
from .responses import SpeakingRequestDetails, SpeakingRequestList

app = FastAPI()
app_config = load_config()
engine = create_engine(app_config.SQLALCHEMY_DATABASE_URI, echo=False)


def get_db_session():
    db = sessionmaker(bind=engine)()

    try:
        yield db
    finally:
        db.close()


@app.get("/health-check/")
def health_check(response: Response):
    alembic_cfg = config.Config()
    alembic_cfg.set_main_option(
        "script_location",
        str(Path(__file__).resolve().parent.parent / "alembic"),
    )
    db_script = script.ScriptDirectory.from_config(alembic_cfg)

    with engine.begin() as connection:
        migration_context = migration.MigrationContext.configure(connection)

        if migration_context.get_current_revision() != db_script.get_current_head():
            response.status_code = 400
            return {"message": "Upgrade the database."}

    return {"message": "OK"}


@app.post("/speaking-requests/", status_code=201, response_model=SpeakingRequestDetails)
def create_speaking_request(
    submit_speaking_request: SubmitSpeakingRequest,
    db_session=Depends(get_db_session),
):
    speaking_request = SpeakingRequest(
        id=str(uuid.uuid4()),
        event_time=submit_speaking_request.event_time,
        address=submit_speaking_request.address,
        topic=submit_speaking_request.topic,
        duration_in_minutes=submit_speaking_request.duration_in_minutes,
        requester_email=submit_speaking_request.requester_email,
        status="PENDING",
    )
    speaking_request = speaking_request_db.save(db_session, speaking_request)
    return speaking_request.model_dump()


@app.get("/speaking-requests/", status_code=200, response_model=SpeakingRequestList)
def list_speaking_requests(db_session=Depends(get_db_session)):
    return {
        "results": [
            speaking_request.model_dump()
            for speaking_request in speaking_request_db.list_all(db_session)
        ]
    }


@app.post(
    "/speaking-requests/accept/",
    status_code=200,
    response_model=SpeakingRequestDetails,
)
def accept_speaking_request(
    accept_speaking_request_body: AcceptSpeakingRequest,
    db_session=Depends(get_db_session),
):
    speaking_request = speaking_request_db.get_by_id(db_session, accept_speaking_request_body.id)
    speaking_request.accept()
    speaking_request = speaking_request_db.save(db_session, speaking_request)

    return speaking_request.model_dump()


@app.post(
    "/speaking-requests/reject/",
    status_code=200,
    response_model=SpeakingRequestDetails,
)
def reject_speaking_request(
    reject_speaking_request_body: RejectSpeakingRequest,
    db_session=Depends(get_db_session),
):
    speaking_request = speaking_request_db.get_by_id(db_session, reject_speaking_request_body.id)
    speaking_request.reject()
    speaking_request = speaking_request_db.save(db_session, speaking_request)

    return speaking_request.model_dump()


@app.post(
    "/ai/review-speaking-request/",
    status_code=200,
    response_model=SpeakingRequestAnalysisResult,
)
async def review_speaking_request(
    submit_speaking_request: SubmitSpeakingRequest,
):
    speaking_request = SpeakingRequest(
        id=str(uuid.uuid4()),
        event_time=submit_speaking_request.event_time,
        address=submit_speaking_request.address,
        topic=submit_speaking_request.topic,
        duration_in_minutes=submit_speaking_request.duration_in_minutes,
        requester_email=submit_speaking_request.requester_email,
        status="PENDING",
    )

    analysis_input = SpeakingRequestAnalysisInput(
        speaking_request=speaking_request,
    )

    return await run_speaking_request_review_with_openai(analysis_input)
