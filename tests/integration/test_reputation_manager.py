
import pytest
from fastapi.testclient import TestClient
from rpg_project.src.api.main import app
from rpg_project.src.services.reputation_manager import ReputationManager
from rpg_project.src.models.enums import EventType


client = TestClient(app)

@pytest.fixture
def rep_manager():
    return ReputationManager("config/factions.json5")


def test_bandit_defeat_changes_reputation(rep_manager):
    char_id = "test_hero"
    # Startwerte aus GDD: city_guard=50, bandits=-50
    state = rep_manager.get_api_state(char_id)
    assert state["city_guard"] == 50
    assert state["bandits"] == -50
    # Event: Bandit besiegt
    rep_manager.handle_event(
        EventType.ON_ENEMY_DEFEATED,
        {"character_id": char_id, "opponent": {"faction": "bandits"}}
    )
    # Erwartung: city_guard +1, bandits -1
    state = rep_manager.get_api_state(char_id)
    assert state["city_guard"] == 51
    assert state["bandits"] == -51
    # API-Call
    response = client.get(f"/api/character/reputation", params={"character_id": char_id})
    assert response.status_code == 200
    data = response.json()
    assert data["city_guard"] == 51
    assert data["bandits"] == -51

def test_no_faction_event_does_nothing(rep_manager):
    char_id = "hero2"
    rep_manager.handle_event(EventType.ON_ENEMY_DEFEATED, {"character_id": char_id, "opponent": {}})
    # Keine Änderung
    state = rep_manager.get_api_state(char_id)
    assert state["city_guard"] == 50
    assert state["bandits"] == -50
