from fastapi.testclient import TestClient
from rpg_project.src.main import app

def test_get_character_stats(monkeypatch):
    # Patch stats_tracker.get_stats, damit ein Dummy-Wert zurückkommt
    from rpg_project.src.api import stats as stats_api
    monkeypatch.setattr(stats_api.stats_tracker, "get_stats", lambda: {"battles": 42, "wins": 21})

    client = TestClient(app)
    resp = client.get("/character/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert data["battles"] == 42
    assert data["wins"] == 21
