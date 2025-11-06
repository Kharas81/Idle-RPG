
import pytest
from fastapi.testclient import TestClient
from rpg_project.src.api.main import app
from rpg_project.src.models.enums import EventType


client = TestClient(app)



def test_bandit_defeat_changes_reputation():
    char_id = "test_hero"
    # Startwerte abfragen
    response = client.get(f"/api/character/reputation", params={"character_id": char_id})
    assert response.status_code == 200
    data = response.json()
    assert data["city_guard"] == 50
    assert data["bandits"] == -50
    # Event: Bandit besiegt (über API)
    event = {
        "event_type": "ON_ENEMY_DEFEATED",
        "data": {"character_id": char_id, "opponent": {"faction": "bandits"}}
    }
    resp = client.post("/api/test/event", json=event)
    assert resp.status_code == 200
    # Erwartung: city_guard +1, bandits -1
    response = client.get(f"/api/character/reputation", params={"character_id": char_id})
    data = response.json()
    assert data["city_guard"] == 51
    assert data["bandits"] == -51

def test_no_faction_event_does_nothing():
    char_id = "hero2"
    # Event ohne Fraktion (über API)
    event = {
        "event_type": "ON_ENEMY_DEFEATED",
        "data": {"character_id": char_id, "opponent": {}}
    }
    resp = client.post("/api/test/event", json=event)
    assert resp.status_code == 200
    # Keine Änderung
    response = client.get(f"/api/character/reputation", params={"character_id": char_id})
    data = response.json()
    assert data["city_guard"] == 50
    assert data["bandits"] == -50
