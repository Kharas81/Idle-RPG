"""
Integrationstest für GameState-API (Sprint S4)
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import pytest
from fastapi.testclient import TestClient
from rpg_project.src.api.game_state import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)

@pytest.fixture
def client():
    return TestClient(app)

def test_get_state(client):
    resp = client.get("/state")
    assert resp.status_code == 200
    data = resp.json()
    assert "tick" in data
    assert "message" in data

def test_tick_and_reset(client):
    # Reset
    resp = client.post("/reset")
    assert resp.status_code == 200
    data = resp.json()
    assert data["tick"] == 0
    # Tick
    resp2 = client.post("/tick")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["tick"] == 1
    # Noch ein Tick
    resp3 = client.post("/tick")
    assert resp3.status_code == 200
    data3 = resp3.json()
    assert data3["tick"] == 2
    # Reset wieder
    resp4 = client.post("/reset")
    assert resp4.status_code == 200
    data4 = resp4.json()
    assert data4["tick"] == 0
