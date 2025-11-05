from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional
from rpg_project.src.services.movement_service import MovementService
from rpg_project.src.services.battle_engine import BattleStore, EntityState
from rpg_project.src.models.world import Tile, WorldMap

router = APIRouter()

class Entity(BaseModel):
    type: str
    x: int
    y: int

class GameState(BaseModel):
    tick: int
    message: str
    width: int
    height: int
    tiles: list
    entities: list
    inventory: list = []

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

def get_worldmap_from_state(state):
    tiles = [Tile(**t) for t in state["tiles"]]
    goal_tile = next((t for t in tiles if t.type == "goal"), None)
    goal = (goal_tile.x, goal_tile.y) if goal_tile else (0, 0)
    return WorldMap(width=state["width"], height=state["height"], tiles=tiles, start=(0,0), goal=goal)

def get_player_pos(state):
    for ent in state["entities"]:
        if ent["type"] == "player":
            return (ent["x"], ent["y"])
    return (0,0)

def set_player_pos(state, pos):
    for ent in state["entities"]:
        if ent["type"] == "player":
            ent["x"], ent["y"] = pos
            break

# Bewegung
@router.post("/move", response_model=GameState)
def move_player(direction: str = Query(..., description="Richtung: up/down/left/right")):
    world = get_worldmap_from_state(game_state)
    pos = get_player_pos(game_state)
    new_pos = MovementService.move(world, pos, direction)
    if new_pos != pos:
        set_player_pos(game_state, new_pos)
        game_state["message"] = f"Spieler bewegt sich {direction}."
    else:
        game_state["message"] = f"Bewegung {direction} nicht möglich."
    return GameState(**game_state)

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
    game_state["message"] = f"Kampf ausgeführt: {status.state}"
    return {"battle": status.dict(), "game_state": GameState(**game_state).dict()}

# Inventar
@router.post("/pickup", response_model=GameState)
def pickup_item():
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

# State, Tick, Reset
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
"""GameState-API: Stellt Endpunkte für Spielzustand, Tick und Reset bereit.
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional
from rpg_project.src.services.movement_service import MovementService
from rpg_project.src.services.battle_engine import BattleStore, EntityState
from rpg_project.src.models.world import Tile, WorldMap

