"""
GameState-API: Stellt Endpunkte für Spielzustand, Tick und Reset bereit.
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any

router = APIRouter()

# Dummy-GameState für Sprint S4 (später GDD-basiert)
class GameState(BaseModel):
    tick: int
    message: str
    # TODO: Später echte Felder wie Map, Charaktere, Inventar etc.

# In-Memory-State (später Session/DB)
game_state = {"tick": 0, "message": "Willkommen im Idle RPG!"}

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
