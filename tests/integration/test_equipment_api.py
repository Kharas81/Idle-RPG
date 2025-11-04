"""Integrationstests für die Equipment-API (/character/equip, /character/unequip)"""
import pytest
from fastapi.testclient import TestClient
from rpg_project.src.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_equip_item_success(client):
    # Nutze jetzt iron_sword als echtes Equipment
    resp = client.post("/character/equip", json={"item_id": "iron_sword"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "weapon" in data["equipment"]
    assert data["stats"]["ATK"] >= 1

def test_equip_item_fail(client):
    resp = client.post("/character/equip", json={"item_id": "not_exist"})
    assert resp.status_code == 400
    assert "Item konnte nicht angelegt werden" in resp.text

def test_unequip_item_success(client):
    # Erst anlegen, dann ablegen (nutze iron_sword als echtes Equipment)
    client.post("/character/equip", json={"item_id": "iron_sword"})
    resp = client.post("/character/unequip", json={"slot": "weapon"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "weapon" not in data["equipment"]

def test_unequip_item_fail(client):
    resp = client.post("/character/unequip", json={"slot": "not_exist"})
    assert resp.status_code == 400
    assert "Slot war leer oder ungültig" in resp.text
