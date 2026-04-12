import datetime

from speakerflow_ai.models import Address, SpeakingRequest


def test_speaking_request_attributes():
    """
    GIVEN id, event time, address, duration in minutes, topic, requester email, status
    WHEN SpeakingRequest is initialized
    THEN it has attributes with the same values
    """
    event_time = datetime.datetime.utcnow()

    speaking_request = SpeakingRequest(
        id="request_id",
        event_time=event_time,
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

    assert speaking_request.id == "request_id"
    assert speaking_request.event_time == event_time
    assert speaking_request.address == Address(
        street="Sunny Street 42",
        city="Dublin",
        state="Leinster",
        country="Ireland",
    )
    assert speaking_request.duration_in_minutes == 45
    assert speaking_request.topic == "Production-ready FastAPI"
    assert speaking_request.requester_email == "john@doe.com"
    assert speaking_request.status == "PENDING"


def test_speaking_request_accept():
    """
    GIVEN a pending speaking request
    WHEN accept is called
    THEN status is set to ACCEPTED
    """
    speaking_request = SpeakingRequest(
        id="request_id",
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

    speaking_request.accept()

    assert speaking_request.status == "ACCEPTED"


def test_speaking_request_reject():
    """
    GIVEN a pending speaking request
    WHEN reject is called
    THEN status is set to REJECTED
    """
    speaking_request = SpeakingRequest(
        id="request_id",
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

    speaking_request.reject()

    assert speaking_request.status == "REJECTED"
