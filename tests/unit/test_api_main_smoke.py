from fastapi.testclient import TestClient
import pytest

# Importiere die FastAPI-App aus main.py
from rpg_project.src.api.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_app_starts(client):
    # Prüfe, ob die App grundsätzlich erreichbar ist (z.B. OpenAPI-Dokumentation)
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    assert resp.json()["openapi"]

def test_api_state_endpoint(client):
    # Prüfe, ob ein zentraler API-Endpunkt erreichbar ist
    resp = client.get("/api/state")
    assert resp.status_code == 200
    data = resp.json()
    assert "tick" in data
    assert "message" in data
