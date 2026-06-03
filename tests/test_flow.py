from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_full_flow():
    # analyzing application
    analysis = client.post(
        "/analyze",
        json={
            "description": "Frontend Developer who knows React and TypeScript",
            "user_skills": ["Python", "FastAPI"],
        },
    )
    assert analysis.status_code == 200

    # save in tracking

    save = client.post(
        "/applications",
        json={"company": "Google", "status": "applied", "match_score": 72},
    )
    assert save.status_code == 200

    # check saved application
    applications = client.get("/applications")
    assert applications.status_code == 200
    assert len(applications.json()) > 0
