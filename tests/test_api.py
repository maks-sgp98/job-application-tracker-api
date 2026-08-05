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


def test_read_applications_returns_empty_list():
    response = client.get("/applications")

    assert response.status_code == 200
    assert response.json() == []


def test_create_application():
    response = client.post(
        "/applications",
        json={
            "company": "Google",
            "position": "Backend Developer",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "company": "Google",
        "position": "Backend Developer",
        "status": "planned",
    }


def test_create_application_rejects_empty_company():
    response = client.post(
        "/applications",
        json={
            "company": "",
            "position": "Backend Developer",
        },
    )

    assert response.status_code == 422


def test_create_application_rejects_empty_position():
    response = client.post(
        "/applications",
        json={
            "company": "Google",
            "position": "",
        },
    )

    assert response.status_code == 422


def test_create_application_rejects_missing_company():
    response = client.post(
        "/applications",
        json={
            "position": "Backend Developer",
        },
    )

    assert response.status_code == 422


def test_create_application_rejects_missing_position():
    response = client.post(
        "/applications",
        json={
            "company": "Google",
        },
    )

    assert response.status_code == 422


def test_read_applications_returns_created_applications():
    client.post(
        "/applications",
        json={
            "company": "Google",
            "position": "Backend Developer",
        },
    )
    client.post(
        "/applications",
        json={
            "company": "REWE",
            "position": "Python Developer",
        },
    )

    response = client.get("/applications")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0] == {
        "id": 1,
        "company": "Google",
        "position": "Backend Developer",
        "status": "planned",
    }
    assert data[1] == {
        "id": 2,
        "company": "REWE",
        "position": "Python Developer",
        "status": "planned",
    }


def test_read_application_returns_application():
    create_response = client.post(
        "/applications",
        json={
            "company": "Google",
            "position": "Backend Developer",
        },
    )

    application_id = create_response.json()["id"]

    response = client.get(f"/applications/{application_id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "company": "Google",
        "position": "Backend Developer",
        "status": "planned",
    }


def test_read_application_returns_404_when_not_found():
    response = client.get("/applications/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Application not found",
    }


def test_read_application_rejects_invalid_id_type():
    response = client.get("/applications/abc")

    assert response.status_code == 422


def test_search_applications_by_company_returns_matches():
    client.post(
        "/applications",
        json={
            "company": "Google",
            "position": "Backend Developer",
        },
    )
    client.post(
        "/applications",
        json={
            "company": "Google Cloud",
            "position": "DevOps Engineer",
        },
    )
    client.post(
        "/applications",
        json={
            "company": "Amazon",
            "position": "Python Developer",
        },
    )

    response = client.get(
        "/applications/search/by-company",
        params={"company": "GOOGLE"},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["company"] == "Google"
    assert data[1]["company"] == "Google Cloud"


def test_search_applications_by_company_returns_empty_list():
    client.post(
        "/applications",
        json={
            "company": "Google",
            "position": "Backend Developer",
        },
    )

    response = client.get(
        "/applications/search/by-company",
        params={"company": "Microsoft"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_search_applications_by_company_rejects_empty_query():
    response = client.get(
        "/applications/search/by-company",
        params={"company": ""},
    )

    assert response.status_code == 422


def test_search_applications_by_company_rejects_missing_query():
    response = client.get("/applications/search/by-company")

    assert response.status_code == 422


def test_update_application_status():
    create_response = client.post(
        "/applications",
        json={
            "company": "Google",
            "position": "Backend Developer",
        },
    )

    application_id = create_response.json()["id"]

    response = client.patch(
        f"/applications/{application_id}/status",
        json={"status": "interview"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "company": "Google",
        "position": "Backend Developer",
        "status": "interview",
    }


def test_update_application_status_is_case_insensitive():
    create_response = client.post(
        "/applications",
        json={
            "company": "Google",
            "position": "Backend Developer",
        },
    )

    application_id = create_response.json()["id"]

    response = client.patch(
        f"/applications/{application_id}/status",
        json={"status": "INTERVIEW"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "interview"


def test_update_application_status_returns_422_for_invalid_status():
    create_response = client.post(
        "/applications",
        json={
            "company": "Google",
            "position": "Backend Developer",
        },
    )

    application_id = create_response.json()["id"]

    response = client.patch(
        f"/applications/{application_id}/status",
        json={"status": "waiting"},
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": "Invalid application status",
    }

    read_response = client.get(f"/applications/{application_id}")

    assert read_response.status_code == 200
    assert read_response.json()["status"] == "planned"


def test_update_application_status_returns_404_when_not_found():
    response = client.patch(
        "/applications/999/status",
        json={"status": "interview"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Application not found",
    }


def test_update_application_status_rejects_empty_status():
    create_response = client.post(
        "/applications",
        json={
            "company": "Google",
            "position": "Backend Developer",
        },
    )

    application_id = create_response.json()["id"]

    response = client.patch(
        f"/applications/{application_id}/status",
        json={"status": ""},
    )

    assert response.status_code == 422


def test_update_application_status_rejects_missing_status():
    create_response = client.post(
        "/applications",
        json={
            "company": "Google",
            "position": "Backend Developer",
        },
    )

    application_id = create_response.json()["id"]

    response = client.patch(
        f"/applications/{application_id}/status",
        json={},
    )

    assert response.status_code == 422


def test_delete_application():
    create_response = client.post(
        "/applications",
        json={
            "company": "Google",
            "position": "Backend Developer",
        },
    )

    application_id = create_response.json()["id"]

    response = client.delete(f"/applications/{application_id}")

    assert response.status_code == 204
    assert response.content == b""

    read_response = client.get(f"/applications/{application_id}")

    assert read_response.status_code == 404


def test_delete_application_returns_404_when_not_found():
    response = client.delete("/applications/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Application not found",
    }


def test_delete_application_rejects_invalid_id_type():
    response = client.delete("/applications/abc")

    assert response.status_code == 422