from fastapi.testclient import TestClient
from rpg_project.src.api.main import app

def test_app_starts():
    client = TestClient(app)
    response = client.get("/api/state")
    assert response.status_code == 200
    data = response.json()
    assert "tick" in data
    assert "entities" in data
