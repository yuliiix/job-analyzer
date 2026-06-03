import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.mark.skip(reason="requires real auth token")
def test_full_flow():
    analysis = client.post(
        "/analyze",
        json={
            "description": "Frontend Developer who knows React and TypeScript",
            "user_skills": ["Python", "FastAPI"],
        },
    )
    assert analysis.status_code == 200

    save = client.post(
        "/applications",
        json={"company": "Google", "status": "applied", "match_score": 72},
    )
    assert save.status_code == 200

    applications = client.get("/applications")
    assert applications.status_code == 200
    assert len(applications.json()) > 0