"""API für BattleEngine: Stellt Endpunkte für Kampfstart, Kampfschritt und Statusabfrage bereit.
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from rpg_project.src.services.battle_engine import BattleStatus, BattleStore, EntityState
from rpg_project.src.services.world_state import WorldState

router = APIRouter()
battle_store = BattleStore()

class StartBattleRequest(BaseModel):
    player: EntityState
    opponent: EntityState

@router.post("/battle/start", response_model=BattleStatus)
def start_battle(req: StartBattleRequest, battle_id: str = Query(..., description="ID für den Kampf")):
    return battle_store.create_battle(battle_id, req.player, req.opponent)

@router.post("/battle/step")
def battle_step(battle_id: str = Query(..., description="ID für den Kampf")):
    try:
        return battle_store.step(battle_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Battle step failed: {str(e)}")

@router.get("/battle/state", response_model=BattleStatus)
def battle_state(battle_id: str = Query(..., description="ID für den Kampf")):
    state = battle_store.get_state(battle_id)
    if not state:
        raise HTTPException(status_code=404, detail="Kein Kampf aktiv")
    return state

# Debugging: Log the entire state of the world
    print(f"WorldState EntityManager state: {world_state.entity_manager._entities}")
    print(f"WorldState components: {world_state.entity_manager._components}")
