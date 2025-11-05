from fastapi import APIRouter
from rpg_project.src.api.game_state_models import GameState
from rpg_project.src.services.battle_engine import BattleStore, EntityState

router = APIRouter()

game_state = None  # Wird im Hauptmodul gesetzt/importiert
battle_store = BattleStore()

@router.post("/battle", response_model=dict)
def do_battle():
    global game_state
    # EntityState aus game_state extrahieren
    def get_entity_state(type_name):
        ent = next((e for e in game_state["entities"] if e["type"] == type_name), None)
        if not ent:
            return None
        hp = ent.get("hp", 10)
        from rpg_project.src.services.battle_engine import EntityState
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

    player = get_entity_state("player")
    opponent = get_entity_state("opponent")
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
