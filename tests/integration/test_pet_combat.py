import pytest
from fastapi.testclient import TestClient
from rpg_project.src.main import app

client = TestClient(app)

# Integrationstest: Pet beschwören und Befehl geben

def test_summon_pet():
    response = client.post("/pet/summon", json={"pet_id": "wolf_pet"})
    assert response.status_code == 200
    data = response.json()
    assert "pet" in data
    assert data["pet"]["name"] == "Wolf"

def test_pet_command():
    # Simuliere einen Kampfumfeld (battle_context kann beliebig erweitert werden)
    response = client.post("/pet/command", json={"pet_id": "wolf_pet", "battle_context": {}})
    assert response.status_code == 200
    data = response.json()
    assert data["action"] == "bite"  # AI wählt immer den ersten Skill
