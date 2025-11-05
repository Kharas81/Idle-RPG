from fastapi import APIRouter
from rpg_project.src.api.game_state_models import GameState

router = APIRouter()

game_state = None  # Wird im Hauptmodul gesetzt/importiert

@router.get("/state", response_model=GameState)
def get_state():
    global game_state
    return GameState(**game_state)

@router.post("/tick", response_model=GameState)
def do_tick():
    global game_state
    game_state["tick"] += 1
    game_state["message"] = f"Tick {game_state['tick']} ausgeführt."
    return GameState(**game_state)

@router.post("/reset", response_model=GameState)
def do_reset():
    global game_state
    game_state["tick"] = 0
    game_state["message"] = "Spiel zurückgesetzt."
    return GameState(**game_state)
