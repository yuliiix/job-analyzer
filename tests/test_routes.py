import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.mark.skip(reason="requires real auth token")
def test_get_applications():
    response = client.get("/applications")
    assert response.status_code == 200


def test_analyze_job():
    response = client.post(
        "/analyze",
        json={
            "description": "Python Developer",
            "user_skills": ["Python", "FastAPI"],
        },
    )
    assert response.status_code == 200


@pytest.mark.skip(reason="requires real auth token")
def test_delete_application():
    response = client.delete("/applications/999")
    assert response.status_code == 200