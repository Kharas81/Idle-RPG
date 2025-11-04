"""GameState-API: Stellt Endpunkte für Spielzustand, Tick und Reset bereit.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# Dummy-GameState für Sprint S4 (später GDD-basiert)


class Entity(BaseModel):
    type: str  # "player", "opponent", "chest" etc.
    x: int
    y: int
    # Optional: id, name, etc.

class GameState(BaseModel):
    tick: int
    message: str
    width: int
    height: int
    tiles: list
    entities: list


# Dummy-Map und Entities für Demo (später GDD/Config-basiert)
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
    ]
}

@router.get("/state", response_model=GameState)
def get_state():
    return GameState(**game_state)

@router.post("/tick", response_model=GameState)
def do_tick():
    game_state["tick"] += 1
    game_state["message"] = f"Tick {game_state['tick']} ausgeführt."
    return GameState(**game_state)

@router.post("/reset", response_model=GameState)
def do_reset():
    game_state["tick"] = 0
    game_state["message"] = "Zurückgesetzt."
    return GameState(**game_state)
