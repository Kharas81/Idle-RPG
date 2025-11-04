import pytest
from fastapi.testclient import TestClient
from rpg_project.src.main import app

client = TestClient(app)

def test_learn_talent_success(monkeypatch):
    # Patch talent_service.learn_talent, damit immer Erfolg zurückkommt
    from rpg_project.src.api import talent as talent_api
    def mock_learn_talent(character, talent_id):
        if talent_id == "talent_01":
            if hasattr(character, "talents"):
                character.talents.append(talent_id)
            else:
                character.talents = [talent_id]
            return True
        return False
    monkeypatch.setattr(talent_api.talent_service, "learn_talent", mock_learn_talent)

    resp = client.post("/character/learn_talent", json={"talent_id": "talent_01"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "talent_01" in data["talents"]

def test_learn_talent_failure(monkeypatch):
    from rpg_project.src.api import talent as talent_api
    def mock_learn_talent(character, talent_id):
        return False
    monkeypatch.setattr(talent_api.talent_service, "learn_talent", mock_learn_talent)

    resp = client.post("/character/learn_talent", json={"talent_id": "invalid_talent"})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Talent konnte nicht freigeschaltet werden."
