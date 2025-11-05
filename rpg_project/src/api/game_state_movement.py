from fastapi import APIRouter, Query
from rpg_project.src.api.game_state_models import GameState
from rpg_project.src.api.game_state_utils import get_worldmap_from_state, get_player_pos, set_player_pos
from rpg_project.src.services.movement_service import MovementService
from rpg_project.src.models.world import Tile, WorldMap

router = APIRouter()

game_state = None  # Wird im Hauptmodul gesetzt/importiert

@router.post("/move", response_model=GameState)
def move_player(direction: str = Query(..., description="Richtung: up/down/left/right")):
    global game_state
    worldmap = get_worldmap_from_state(game_state)
    pos = get_player_pos(game_state)
    new_pos = MovementService.move(pos, direction, worldmap)
    set_player_pos(game_state, new_pos)
    return GameState(**game_state)
