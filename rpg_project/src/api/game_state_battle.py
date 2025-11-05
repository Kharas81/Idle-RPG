from fastapi import APIRouter
from rpg_project.src.api.game_state_models import GameState
from rpg_project.src.services.battle_engine import BattleStore, EntityState

router = APIRouter()

game_state = None  # Wird im Hauptmodul gesetzt/importiert
battle_store = BattleStore()

@router.post("/battle", response_model=dict)
def do_battle():
    global game_state
    player = next((e for e in game_state["entities"] if e["type"] == "player"), None)
    opponent = next((e for e in game_state["entities"] if e["type"] == "opponent"), None)
    if not player or not opponent:
        return {"error": "Spieler oder Gegner nicht gefunden", "game_state": GameState(**game_state).dict()}
    status = battle_store.battle(player, opponent)
    return {"battle": status.dict(), "game_state": GameState(**game_state).dict()}
