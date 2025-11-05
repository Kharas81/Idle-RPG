import pytest
from rpg_project.src.api.game_state_utils import get_worldmap_from_state, get_player_pos, set_player_pos

# Beispiel-Spielzustand für Tests
@pytest.fixture
def example_state():
    return {
        "width": 5,
        "height": 5,
        "tiles": [
            {"x": 0, "y": 0, "type": "start"},
            {"x": 1, "y": 0, "type": "goal"},
            {"x": 2, "y": 0, "type": "floor"},
        ],
        "entities": [
            {"type": "player", "x": 1, "y": 2},
            {"type": "opponent", "x": 2, "y": 2}
        ],
        "inventory": []
    }

def test_get_worldmap_from_state(example_state):
    worldmap = get_worldmap_from_state(example_state)
    assert worldmap.width == 5
    assert worldmap.height == 5
    assert len(worldmap.tiles) == 3
    assert worldmap.goal == (1, 0)

def test_get_player_pos(example_state):
    pos = get_player_pos(example_state)
    assert pos == (1, 2)

def test_get_player_pos_no_player():
    state = {"entities": []}
    pos = get_player_pos(state)
    assert pos == (0, 0)

def test_set_player_pos(example_state):
    set_player_pos(example_state, (3, 4))
    pos = get_player_pos(example_state)
    assert pos == (3, 4)

def test_set_player_pos_invalid(example_state):
    set_player_pos(example_state, "invalid")
    pos = get_player_pos(example_state)
    assert pos == (1, 2)  # unverändert

def test_get_worldmap_from_state_missing_fields():
    state = {}
    worldmap = get_worldmap_from_state(state)
    assert worldmap.width == 0
    assert worldmap.height == 0
    assert worldmap.goal == (0, 0)
    assert worldmap.tiles == []
