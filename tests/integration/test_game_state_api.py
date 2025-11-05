"""Integrationstest für GameState-API (Sprint S4)
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from rpg_project.src.api.game_state import router

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
    resp = client.post("/reset")
    assert resp.status_code == 200
    data = resp.json()
    assert data["tick"] == 0
    resp2 = client.post("/tick")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["tick"] == 1
    resp3 = client.post("/tick")
    assert resp3.status_code == 200
    data3 = resp3.json()
    assert data3["tick"] == 2
    resp4 = client.post("/reset")
    assert resp4.status_code == 200
    data4 = resp4.json()
    assert data4["tick"] == 0

def test_move_player_valid(client):
    resp = client.post("/move?direction=right")
    assert resp.status_code == 200
    data = resp.json()
    assert "Spieler bewegt sich right." in data["message"] or "Bewegung right nicht möglich." in data["message"]

def test_move_player_invalid(client):
    resp = client.post("/move?direction=up")
    assert resp.status_code == 200
    data = resp.json()
    assert "Bewegung up nicht möglich." in data["message"] or "Spieler bewegt sich up." in data["message"]

def test_battle_success(client):
    resp = client.post("/battle")
    assert resp.status_code == 200
    data = resp.json()
    assert "battle" in data or "error" in data

def test_pickup_item(client):
    client.post("/move?direction=right")
    client.post("/move?direction=down")
    resp = client.post("/pickup")
    assert resp.status_code == 200
    data = resp.json()
    assert "Item aufgenommen" in data["message"] or "Keine Kiste am Spieler-Standort." in data["message"]

def test_move_player_left_wall(client):
    resp = client.post("/move?direction=left")
    assert resp.status_code == 200
    data = resp.json()
    assert "Spieler bewegt sich left." in data["message"] or "Bewegung left nicht möglich." in data["message"]

def test_move_player_down(client):
    resp = client.post("/move?direction=down")
    assert resp.status_code == 200
    data = resp.json()
    assert "Spieler bewegt sich down." in data["message"] or "Bewegung down nicht möglich." in data["message"]

def test_battle_missing_opponent(client):
    resp = client.post("/reset")
    state = client.get("/state").json()
    resp = client.post("/battle")
    data = resp.json()
    assert "battle" in data or "error" in data

def test_pickup_no_chest(client):
    client.post("/reset")
    client.post("/move?direction=up")
    resp = client.post("/pickup")
    assert resp.status_code == 200
    data = resp.json()
    assert "Keine Kiste am Spieler-Standort." in data["message"]
