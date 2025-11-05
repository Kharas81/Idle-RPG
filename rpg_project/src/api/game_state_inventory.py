from fastapi import APIRouter
from rpg_project.src.api.game_state_models import GameState
from rpg_project.src.api.game_state_utils import get_player_pos

router = APIRouter()

game_state = None  # Wird im Hauptmodul gesetzt/importiert

@router.post("/pickup", response_model=GameState)
def pickup_item():
    global game_state
    player_pos = get_player_pos(game_state)
    chest = next((e for e in game_state["entities"] if e["type"] == "chest"), None)
    if chest and (chest["x"], chest["y"]) == player_pos:
        item = {"item_id": "potion", "qty": 1}
        game_state["inventory"].append(item)
        game_state["message"] = "Item aufgenommen: potion"
        game_state["entities"] = [e for e in game_state["entities"] if e["type"] != "chest"]
    else:
        game_state["message"] = "Keine Kiste am Spieler-Standort."
    return GameState(**game_state)
