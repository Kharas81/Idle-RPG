import sys
import os
import tempfile
import shutil
import pytest
from fastapi.testclient import TestClient

# sys.path-Anpassung für lokale Imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from rpg_project.src.main import app

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def cleanup_sessions():
    # Vor jedem Test: sessions-Verzeichnis leeren
    sessions_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../rpg_project/sessions'))
    if os.path.exists(sessions_dir):
        shutil.rmtree(sessions_dir)
    os.makedirs(sessions_dir, exist_ok=True)
    yield
    # Nach jedem Test: sessions-Verzeichnis leeren
    if os.path.exists(sessions_dir):
        shutil.rmtree(sessions_dir)


def test_session_lifecycle():
    session_id = "testsession1"
    initial_state = {"player": {"name": "Hero", "level": 1}, "progress": 0}
    # Neue Session anlegen
    resp = client.post("/session/new", json={"session_id": session_id, "initial_state": initial_state})
    assert resp.status_code == 200
    # Session speichern (Update)
    updated_state = {"player": {"name": "Hero", "level": 2}, "progress": 42}
    resp = client.post("/session/save", json={"session_id": session_id, "state": updated_state})
    assert resp.status_code == 200
    # Session laden
    resp = client.get(f"/session/load?session_id={session_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["state"] == updated_state


def test_load_nonexistent_session():
    resp = client.get("/session/load?session_id=doesnotexist")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Session not found"
