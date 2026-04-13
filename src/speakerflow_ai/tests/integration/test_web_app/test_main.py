import pytest
from fastapi.testclient import TestClient

from speakerflow_ai.web_app.main import app


@pytest.fixture
def client(database_engine):
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
