import pytest
from fastapi.testclient import TestClient

from app.api import app
from app.services import reset_applications


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    reset_applications()
    yield
    reset_applications()

def test_read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Job Application Tracker API",
        "status": "running",
    }

def test_create_application():
    response = client.post(
        "/applications",
        json={
            "company": "Google",
            "position": "Backend Developer",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["company"] == "Google"
    assert data["position"] == "Backend Developer"
    assert data["status"] == "planned"

def test_read_application_returns_404_when_not_found():
    response = client.get("/applications/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Application not found",
    }