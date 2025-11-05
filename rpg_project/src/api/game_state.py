from fastapi import APIRouter, Query
from rpg_project.src.services.movement_service import MovementService
from rpg_project.src.services.battle_engine import BattleStore, EntityState
from rpg_project.src.models.world import Tile, WorldMap
from rpg_project.src.api.game_state_models import Entity, GameState
from typing import Optional

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


# Kampf
battle_store = BattleStore()
def get_entity_state_from_game(type_name: str) -> Optional[EntityState]:
    ent = next((e for e in game_state["entities"] if e["type"] == type_name), None)
    if not ent:
        return None
    hp = ent.get("hp", 10)
    return EntityState(
        id=type_name,
        name=type_name,
        hp=hp,
        max_hp=10,
        atk=3 if type_name=="player" else 2,
        defense=1 if type_name=="player" else 0,
        is_player=(type_name=="player"),
        effects=[],
        mana=100
    )

@router.post("/battle", response_model=dict)
def do_battle():
    player = get_entity_state_from_game("player")
    opponent = get_entity_state_from_game("opponent")
    if not player or not opponent:
        return {"error": "Spieler oder Gegner nicht gefunden", "game_state": GameState(**game_state).dict()}
    battle_id = f"demo-battle-{game_state['tick']}"
    battle_store.create_battle(battle_id, player, opponent)
    status = battle_store.step(battle_id)
    for ent in game_state["entities"]:
        if ent["type"] == "player":
            ent["hp"] = status.entities["player"].hp
        if ent["type"] == "opponent":
            ent["hp"] = status.entities["opponent"].hp
"""GameState-API: Stellt Endpunkte für Spielzustand, Tick und Reset bereit.
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional
from rpg_project.src.services.movement_service import MovementService
from rpg_project.src.services.battle_engine import BattleStore, EntityState
from rpg_project.src.models.world import Tile, WorldMap

