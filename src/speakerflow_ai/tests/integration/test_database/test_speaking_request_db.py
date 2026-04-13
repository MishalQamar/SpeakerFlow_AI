import datetime
import uuid

from speakerflow_ai.database import speaking_request_db
from speakerflow_ai.models import Address, SpeakingRequest


def test_speaking_request_save_and_fetch(database_session):
    """
    GIVEN a speaking request and a database session
    WHEN the speaking request is saved
    THEN it can be listed and fetched by id
    """
    speaking_request = SpeakingRequest(
        id=str(uuid.uuid4()),
        event_time=datetime.datetime.utcnow(),
        address=Address(
            street="Sunny Street 42",
            city="Dublin",
            state="Leinster",
            country="Ireland",
        ),
        duration_in_minutes=45,
        topic="Production-ready FastAPI",
        requester_email="john@doe.com",
        status="PENDING",
    )

    speaking_request_db.save(database_session, speaking_request)

    assert speaking_request_db.list_all(database_session)[0] == speaking_request
    assert speaking_request_db.get_by_id(database_session, speaking_request.id) == speaking_request
