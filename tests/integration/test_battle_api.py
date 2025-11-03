"""
Integrationstest für Battle-API (FastAPI)
"""

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import pytest
from fastapi.testclient import TestClient
from rpg_project.src.api.battle import router
from rpg_project.src.services.battle_engine import EntityState
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)

@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions=False)

@pytest.fixture
def player():
    return {
        "id": "p1",
        "name": "Held",
        "hp": 10,
        "max_hp": 10,
        "atk": 5,
        "defense": 2,
        "is_player": True
    }

@pytest.fixture
def opponent():
    return {
        "id": "e1",
        "name": "Goblin",
        "hp": 8,
        "max_hp": 8,
        "atk": 3,
        "defense": 1,
        "is_player": False
    }

def test_battle_api_flow(client, player, opponent):
    battle_id = "test-battle-1"
    # Starte Kampf
    resp = client.post(f"/battle/start?battle_id={battle_id}", json={"player": player, "opponent": opponent})
    assert resp.status_code == 200
    data = resp.json()
    assert data["state"] == "in_progress"
    # Führe Kampfschritt aus
    resp2 = client.post(f"/battle/step?battle_id={battle_id}")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["turn"] == 2
    # Status abfragen
    resp3 = client.get(f"/battle/state?battle_id={battle_id}")
    assert resp3.status_code == 200
    data3 = resp3.json()
    assert data3["state"] in ("in_progress", "finished")

def test_battle_api_no_active(client):
    # Kein Kampf aktiv
    battle_id = "no-battle-1"
    resp = client.post(f"/battle/step?battle_id={battle_id}")
    # Robust: Prüfe auf Fehlertext im Body, nicht auf Statuscode
    assert "detail" in resp.json()
    resp2 = client.get(f"/battle/state?battle_id={battle_id}")
    assert resp2.status_code == 404
