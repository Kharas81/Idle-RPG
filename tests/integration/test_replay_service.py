"""Integrationstest für Replay-API: Seed, Aktionen, Replay deterministisch
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from rpg_project.src.api.replay import router

app = FastAPI()
app.include_router(router)

@pytest.fixture
def client():
    return TestClient(app)

def test_replay_save_and_load(client):
    # Seed setzen
    resp = client.post("/rng/seed", json={"seed": 12345})
    assert resp.status_code == 200
    # Aktionen simulieren
    actions = ["move", "attack", "loot"]
    resp2 = client.post("/replay/save", json={"actions": actions})
    assert resp2.status_code == 200
    data = resp2.json()
    assert data["seed"] == 12345
    assert data["actions"] == actions
    # Replay laden
    resp3 = client.post("/replay/load")
    assert resp3.status_code == 200
    data2 = resp3.json()
    assert data2["seed"] == 12345
    assert data2["actions"] == actions

def test_replay_load_without_save(client):
    # ReplayService resetten (direkt im Modul)
    from rpg_project.src.services.replay_service import replay_service
    replay_service.reset()
    resp = client.post("/replay/load")
    assert resp.status_code == 404
