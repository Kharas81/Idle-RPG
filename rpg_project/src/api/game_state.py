
"""
game_state.py
Zentrale API-Initialisierung und globale Spielzustandsverwaltung für das Idle-RPG.
Nur Routing, Initialisierung und zentrale Logik. Alle Hilfsfunktionen und Modelle sind ausgelagert.
"""

from fastapi import APIRouter
from rpg_project.src.api.game_state_models import Entity, GameState
from rpg_project.src.api.game_state_utils import get_worldmap_from_state, get_player_pos, set_player_pos

router = APIRouter()

router = APIRouter()

from rpg_project.src.api.game_state_models import Entity, GameState

game_state = {
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
        {"type": "player", "x": 1, "y": 1},
        {"type": "opponent", "x": 3, "y": 2},
        {"type": "chest", "x": 2, "y": 2}
    ],
    "inventory": []
}

from rpg_project.src.api.game_state_utils import get_worldmap_from_state, get_player_pos, set_player_pos


## Kampflogik ist ausgelagert nach game_state_battle.py


## Alle Endpunkte und Logik für Battle sind ausgelagert nach game_state_battle.py

