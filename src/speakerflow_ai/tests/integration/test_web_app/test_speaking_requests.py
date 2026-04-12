import pytest
from fastapi.testclient import TestClient

from speakerflow_ai.web_app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    """
    GIVEN the web app is running
    WHEN the health check endpoint is called with GET
    THEN a 200 response with message OK is returned
    """
    response = client.get("/health-check/")
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}


def test_create_speaking_request(client):
    """
    GIVEN event time, address, topic, duration in minutes, requester email
    WHEN the create speaking request endpoint is called
    THEN a speaking request with the same attributes is returned
    """
    response = client.post(
        "/request-speaking/",
        json={
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
        },
    )

    assert response.status_code == 201

    response_body = response.json()
    assert isinstance(response_body["id"], str)
    assert response_body["event_time"] == "2026-05-10T14:30:00"
    assert response_body["address"] == {
        "street": "Sunny Street 42",
        "city": "Dublin",
        "state": "Leinster",
        "country": "Ireland",
    }
    assert response_body["topic"] == "Production-ready FastAPI"
    assert response_body["duration_in_minutes"] == 45
    assert response_body["requester_email"] == "john@doe.com"
    assert response_body["status"] == "PENDING"
