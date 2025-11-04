from rpg_project.src.main import app, run_gameloop
from fastapi.testclient import TestClient
import pytest

def test_fastapi_app_root():
    client = TestClient(app)
    # Teste, ob die App grundsätzlich läuft (z.B. 404 für nicht vorhandene Route)
    resp = client.get("/doesnotexist")
    assert resp.status_code == 404

def test_run_gameloop(capsys):
    # Teste, ob die GameLoop-Funktion ohne Fehler durchläuft und erwartete Ausgaben erzeugt
    run_gameloop()
    out = capsys.readouterr().out
    assert "Startposition" in out
    assert "Endposition" in out
    assert "Move right" in out
