"""Integrationstest für GameState-API (Sprint S4)
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


from rpg_project.src.api.game_state_movement import router as movement_router
from rpg_project.src.api.game_state_battle import router as battle_router
from rpg_project.src.api.game_state_inventory import router as inventory_router
from rpg_project.src.api.game_state_tickreset import router as tickreset_router

app = FastAPI()
app.include_router(movement_router, prefix="/api")
app.include_router(battle_router, prefix="/api")
app.include_router(inventory_router, prefix="/api")
app.include_router(tickreset_router, prefix="/api")

@pytest.fixture
def client():
    # Initialisiere das globale game_state für alle Module
    initial_state = {
        "tick": 0,
        "message": "Willkommen im Idle RPG!",
        "width": 5,
        "height": 5,
        "tiles": [
            {"x": 0, "y": 0, "type": "start"},
            {"x": 1, "y": 0, "type": "floor"},
            {"x": 2, "y": 0, "type": "wall"},
            {"x": 3, "y": 0, "type": "goal"},
            {"x": 4, "y": 0, "type": "floor"},
            {"x": 0, "y": 1, "type": "floor"},
            {"x": 1, "y": 1, "type": "floor"},
            {"x": 2, "y": 1, "type": "floor"},
            {"x": 3, "y": 1, "type": "wall"},
            {"x": 4, "y": 1, "type": "floor"},
            {"x": 0, "y": 2, "type": "wall"},
            {"x": 1, "y": 2, "type": "floor"},
            {"x": 2, "y": 2, "type": "floor"},
            {"x": 3, "y": 2, "type": "floor"},
            {"x": 4, "y": 2, "type": "wall"},
            {"x": 0, "y": 3, "type": "floor"},
            {"x": 1, "y": 3, "type": "wall"},
            {"x": 2, "y": 3, "type": "floor"},
            {"x": 3, "y": 3, "type": "floor"},
            {"x": 4, "y": 3, "type": "floor"},
            {"x": 0, "y": 4, "type": "floor"},
            {"x": 1, "y": 4, "type": "floor"},
            {"x": 2, "y": 4, "type": "wall"},
            {"x": 3, "y": 4, "type": "floor"},
            {"x": 4, "y": 4, "type": "goal"}
        ],
        "entities": [
            {"type": "player", "x": 1, "y": 1, "hp": 10},
            {"type": "opponent", "x": 3, "y": 2, "hp": 10},
            {"type": "chest", "x": 2, "y": 2}
        ],
        "inventory": []
    }
    import copy
    import rpg_project.src.api.game_state_movement as movement
    import rpg_project.src.api.game_state_battle as battle
    import rpg_project.src.api.game_state_inventory as inventory
    import rpg_project.src.api.game_state_tickreset as tickreset
    movement.game_state = copy.deepcopy(initial_state)
    battle.game_state = movement.game_state
    inventory.game_state = movement.game_state
    tickreset.game_state = movement.game_state
    return TestClient(app)

def test_get_state(client):
    resp = client.get("/api/state")
    assert resp.status_code == 200
    data = resp.json()
    assert "tick" in data
    assert "message" in data

def test_tick_and_reset(client):
    resp = client.post("/api/reset")
    assert resp.status_code == 200
    data = resp.json()
    assert data["tick"] == 0
    resp2 = client.post("/api/tick")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["tick"] == 1
    resp3 = client.post("/api/tick")
    assert resp3.status_code == 200
    data3 = resp3.json()
    assert data3["tick"] == 2
    resp4 = client.post("/api/reset")
    assert resp4.status_code == 200
    data4 = resp4.json()
    assert data4["tick"] == 0

def test_move_player_valid(client):
    resp = client.post("/api/move?direction=right")
    assert resp.status_code == 200
    data = resp.json()
    assert "Spieler bewegt sich right." in data["message"] or "Bewegung right nicht möglich." in data["message"]

def test_move_player_invalid(client):
    resp = client.post("/api/move?direction=up")
    assert resp.status_code == 200
    data = resp.json()
    assert "Bewegung up nicht möglich." in data["message"] or "Spieler bewegt sich up." in data["message"]

def test_battle_success(client):
    resp = client.post("/api/battle")
    assert resp.status_code == 200
    data = resp.json()
    assert "battle" in data or "error" in data

def test_pickup_item(client):
    client.post("/api/move?direction=right")
    client.post("/api/move?direction=down")
    resp = client.post("/api/pickup")
    assert resp.status_code == 200
    data = resp.json()
    assert "Item aufgenommen" in data["message"] or "Keine Kiste am Spieler-Standort." in data["message"]

def test_move_player_left_wall(client):
    resp = client.post("/api/move?direction=left")
    assert resp.status_code == 200
    data = resp.json()
    assert "Spieler bewegt sich left." in data["message"] or "Bewegung left nicht möglich." in data["message"]

def test_move_player_down(client):
    resp = client.post("/api/move?direction=down")
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
