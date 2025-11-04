import pytest
from fastapi.testclient import TestClient
from rpg_project.src.main import app

client = TestClient(app)

def test_interact_with_object_success(monkeypatch):
    # Patch INTERACTION_SERVICE.interact, damit immer Erfolg zurückkommt
    from rpg_project.src.api import interaction as interaction_api
    def mock_interact(character, interactable_id):
        return {"success": True, "loot": ["gold"]}
    monkeypatch.setattr(interaction_api.INTERACTION_SERVICE, "interact", mock_interact)

    resp = client.post("/action/interact", json={"character_id": "char1", "interactable_id": "chest1"})
    assert resp.status_code == 200
    assert resp.json()["success"] is True
    assert "loot" in resp.json()

def test_interact_with_object_failure(monkeypatch):
    from rpg_project.src.api import interaction as interaction_api
    def mock_interact(character, interactable_id):
        return {"success": False, "error": "locked"}
    monkeypatch.setattr(interaction_api.INTERACTION_SERVICE, "interact", mock_interact)

    resp = client.post("/action/interact", json={"character_id": "char1", "interactable_id": "chest1"})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "locked"
